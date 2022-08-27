from discord.ext import commands
import subprocess

DICT_PATH="../dict.txt"


async def addDict(arg1,arg2):
    #辞書ファイルの末尾に追記
    with open(DICT_PATH, mode='a') as f:
        f.write(arg1 + ',' + arg2+'\n')


def replaceDict(text):
    #辞書に基づいて置換
    f = open(DICT_PATH, 'r')
    lines = f.readlines()
    print(lines)
    for line in lines:
        pattern = line.strip().split(',')
        if pattern[0] in text and len(pattern) >= 2:
            text = text.replace(pattern[0], pattern[1])
    f.close()
    return text


def showDict():
    #辞書を読み込んで表示
    f = open(DICT_PATH, 'r')
    lines = f.readlines()
    output = "現在登録されている辞書一覧\n"
    for index, line in enumerate(lines):
        pattern = line.strip().split(',')
        output += "{0}: {1} -> {2}\n".format(index+1,pattern[0],pattern[1])
    f.close()
    return output

async def removeDict(num):
    #辞書の削除
    try:
        cmd = ["sed", "-i.bak","-e", ("{0}d").format(num),"dict.txt"]
        subprocess.call(cmd)
    except Exception as e:
        print(e)
        return 0
    return 1


class DictCog(commands.Cog):
    #辞書管理用のコマンドを集めたコグ
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def get(self,ctx):
        #辞書を表示(!get)
        await ctx.channel.send(showDict())
    
    @commands.command()
    async def add(self,ctx,a,b):
        #辞書に追加(!add xxx yyy)
        if len(a) > 10 or len(b) > 10:
            await ctx.channel.send("荒らしは許されませんよ♡")
            return
        await addDict(a,b)
        await ctx.channel.send(("{0}を{1}と読むように辞書に登録しました！").format(a,b))

    @commands.command()
    async def remove(self,ctx,num):
        #辞書を削除(!remove 3)
        if await removeDict(num):
            await ctx.channel.send("削除しました")
        else:
            await ctx.channel.send("エラーが発生しました")


#Cogとして使うのに必要なsetup関数
def setup(bot):
    print("DictCog OK")
    return bot.add_cog(DictCog(bot))