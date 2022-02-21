import discord
import os
import asyncio
from webserver import alive
from discord.ext import commands
from discord.ext import tasks

PING_DELAY = 300
GAME = 'elite dangerous'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!ngi'),
                   discription='NO GENSHIN IMPACT',
                   intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('logged on as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name='NO GENSHIN IMPACT'))


@tasks.loop(seconds=10)
async def look_for_genshin_players():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(os.getenv('ANNOUNCEMENTS')))

    while not bot.is_closed():
        for member in bot.get_all_members():
            if member.activity != None:
                if member.activity.name.lower().find(GAME) != -1:
                    title = 'EW {} IS PLAYING GENSHIN IMPACT'.format(member)
                    desc = '{} PLEASE TAKE A SHOWER IMMEDIATELY'.format(
                        member.mention)
                    file = discord.File('./resources/shower.gif')
                    await channel.send(member.mention)
                    await channel.send(embed=discord.Embed(
                        title=title, description=desc, color=0xEE4B2B
                    ), file=file)
        await asyncio.sleep(PING_DELAY)


def main():
    print('starting bot')
    alive()
    look_for_genshin_players.start()
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
