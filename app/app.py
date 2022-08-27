import os
import discord
from app.util.yomiage import play_process, read_message

from util.dict_cog import DictCog
from util.yomiage_setting_cog import YomiageSettingCog
from util.yomiage import play_process

#discord.Botはdiscord.Clientを継承したサブクラスなので多分大丈夫
client = discord.Bot(command_prefix="!") 
client_id = os.environ['DISCORD_CLIENT_ID']

#コグの追加
client.add_cog(YomiageSettingCog(client))
client.add_cog(DictCog(client))

#コグからの情報の取得
yomiage=client.get_cog("YomiageSettingCog")

# GUILD_ID=833346660201398282
# guild = client.get_guild(GUILD_ID)

async def get_client():
    #クライアントのオブジェクト取得用
    await client

@client.event
async def on_ready():
    # 起動時の処理
    print('Bot is wake up.')

@client.command()
async def bye():
    #さよなら
    await client.close()

@client.event
async def on_message(message):
    yomiage.volume = 0.5
    #ここボリューム上で定義してるからいらなくね？
    if yomiage.voice and yomiage.volume is None:
        source = discord.PCMVolumeTransformer(yomiage.voice.source)
        yomiage.volume = source.volume
    #ボット排除＆チャンネル判断
    if not message.author.bot and message.channel == yomiage.currentChannel :
        read_message(message,yomiage.currentChannel)
    #コマンド側にメッセージを渡す
    await client.process_commands(message)
        
@client.event
async def on_voice_state_update(
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState):
        #VCの状態が変わった時に呼び出される

        if not before.channel and after.channel :
            msgtxt=member.display_name +"さんこんにちは！"
        elif before.channel and not after.channel:
            msgtxt=member.display_name +"さんが退出しました"
        else :return

        play_process(msgtxt,member.guild,member.guild.voice_client)


#トークンを入れて実行！
client.run(client_id)
