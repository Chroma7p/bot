import os
import re
import time
import discord
import subprocess
from threading import Timer
from dict_cog import DICT_PATH
from collections import defaultdict, deque
from ..app import get_client

url = re.compile('^http')
mention = re.compile('<@[^>]*>*')
queue_dict = defaultdict(deque)


def replaceDict(text):
    #テキストを置換
    f = open(DICT_PATH, 'r')
    lines = f.readlines()
    print(lines)

    for line in lines:
        pattern = line.strip().split(',')
        if pattern[0] in text and len(pattern) >= 2:
            text = text.replace(pattern[0], pattern[1])
    f.close()
    return text


async def replaceUserName(text):
    #ユーザー名を置換
    for word in text.split():
        if not mention.match(word):
            continue
        userId = re.sub('[<@!> ]', '', word)
        print(userId)
        userName = str(await get_client().fetch_user(userId))
        # nickName = str(await guild.get_member_named(userName))
        # print(nickName)
        # userName = '砂糖#'
        userName = re.sub('#.*', '', userName)
        text = text.replace(word, '@'+userName)
    return text


async def read_message(message,currentChannel):
    #受け取ったメッセージを読み上げる
    text = message.content
    print( message.channel,currentChannel)
    if message.guild.voice_client:
        print(message.author)
        if mention.search(text):
            text = await replaceUserName(text)
        text = re.sub('#.*','',str(message.author.display_name)) + text
        text = re.sub('http.*', '', text)
        text = replaceDict(text)
        if len(text) > 100:
            await message.channel.send("文字数が長すぎるよ")
            return
        play_process(text,message.guild,message.guild.voice_client)


async def play_process(text,send_to,voice_client):
    #音声を合成して、キューに突っ込む
    filename = await jtalk(text)
    if os.path.getsize(filename) > 10000000:
            await send_to.send("再生時間が長すぎるよ")
            return
    enqueue(voice_client, send_to,
                discord.FFmpegPCMAudio(filename),filename)
    timer = Timer(3, os.remove, (filename, ))
    timer.start()


async def jtalk(t):
    #subprocessでコマンド叩いて音声合成してファイル名を返す
    open_jtalk = ['open_jtalk']
    mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m', '/usr/share/hts-voice/mei/mei_normal.htsvoice']
    pitch = ['-fm', '-5']
    speed = ['-r', '1.0']
    file = str(round(time.time() * 1000))
    outwav = ['-ow', file + '.wav']
    cmd = open_jtalk+mech+htsvoice+pitch+speed+outwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    return file + '.wav'


def enqueue(voice_client, guild, source,filename):
    #キューに突っ込む
    queue = queue_dict[guild.id]
    queue.append([source,filename])
    if not voice_client.is_playing():
        play(voice_client, queue)


def play(voice_client, queue):
    #キューを一個ずつ再生
    if not queue or voice_client.is_playing():
        return
    source = queue.popleft()
    # os.remove(source[1])
    voice_client.play(source[0], after=lambda e: play(voice_client, queue))