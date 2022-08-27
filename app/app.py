import os
import discord
from app.util.yomiage import play_process, read_message

from util.dict_cog import DictCog
from util.yomiage_setting_cog import YomiageSettingCog
from util.yomiage import play_process


client = discord.Bot(command_prefix="!") #discord.Botはdiscord.Clientを継承したサブクラスなので多分大丈夫
client_id = os.environ['DISCORD_CLIENT_ID']
client.add_cog(YomiageSettingCog(client))
client.add_cog(DictCog(client))
yomiage=client.get_cog("YomiageSettingCog")

# GUILD_ID=833346660201398282
# guild = client.get_guild(GUILD_ID)

async def get_client():
    await client

@client.event
async def on_ready():
    # 起動時の処理
    print('Bot is wake up.')


@client.command()
async def bye():
    await client.close()

@client.event
async def on_message(message):
    yomiage.volume = 0.5
    #ここボリューム上で定義してるからいらなくね？
    if yomiage.voice and yomiage.volume is None:
        source = discord.PCMVolumeTransformer(yomiage.voice.source)
        yomiage.volume = source.volume

    if not message.author.bot and message.channel == yomiage.currentChannel :
        read_message(message,yomiage.currentChannel)
    await client.process_commands(message)
        
@client.event
async def on_voice_state_update(
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState):

        if not before.channel and after.channel :
            msgtxt=member.display_name +"さんこんにちは！"
        elif before.channel and not after.channel:
            msgtxt=member.display_name +"さんが退出しました"
        else :return

        play_process(msgtxt,member.guild,member.guild.voice_client)

client.run(client_id)
