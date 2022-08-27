from discord.ext import commands


#読み上げに関する設定をまとめたコグ
#＠commands.command()をつければコマンドになる
#基本的に関数名がコマンド名になる
class YomiageSettingCog(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.voice=None
        self.volume=None
        self.currentChannel=None

    @commands.command()
    async def join(self,ctx):
        self.currentChannel = ctx.channel
        self.voice = await ctx.channel.connect()
        await ctx.channel.send('ボイスチャンネルにログインしました')

    @commands.command()
    async def dc(self,ctx):
        await self.voice.disconnect()
        self.currentChannel = None
        await ctx.channel.send('ボイスチャンネルからログアウトしました')

    @commands.command()
    async def status(self,ctx):
        if self.voice.is_connected():
            await ctx.channel.send('ボイスチャンネルに接続中です')

    @commands.command()
    async def vol(self,ctx,arg=""):
        send=""
        if arg=="up":
            self.volume+=0.1
            send+="音量を上げました\n"
        elif arg=="down":
            self.volume-=0.1
            send+="音量を下げました\n"
        await ctx.channel.send(send+f"現在の音量は{self.volume}です")



#Cogとして使うのに必要なsetup関数
def setup(bot):
    print("YomiageCog OK")
    return bot.add_cog(YomiageSettingCog(bot))