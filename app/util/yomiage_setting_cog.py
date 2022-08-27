from discord.ext import commands

class YomiageSettingCog(commands.Cog):
    #読み上げに関する設定をまとめたコグ
    #voice
    def __init__(self,bot):
        self.bot=bot
        self.voice=None
        self.volume=None
        self.currentChannel=None

    @commands.command()
    async def join(self,ctx):
        #VCにログイン
        self.currentChannel = ctx.channel
        self.voice = await ctx.channel.connect()
        await ctx.channel.send('ボイスチャンネルにログインしました')

    @commands.command()
    async def dc(self,ctx):
        #VCからログアウト
        await self.voice.disconnect()
        self.currentChannel = None
        await ctx.channel.send('ボイスチャンネルからログアウトしました')

    @commands.command()
    async def status(self,ctx):
        #状態の表示
        if self.voice.is_connected():
            await ctx.channel.send('ボイスチャンネルに接続中です')

    @commands.command()
    async def vol(self,ctx,arg=""):
        #音量調整
        send=""
        if arg=="up":
            self.volume+=0.1
            send+="音量を上げました\n"
        elif arg=="down":
            self.volume-=0.1
            send+="音量を下げました\n"
        await ctx.channel.send(send+f"現在の音量は{self.volume}です")


def setup(bot):
    #Cogとして使うのに必要なsetup関数
    print("YomiageCog OK")
    return bot.add_cog(YomiageSettingCog(bot))