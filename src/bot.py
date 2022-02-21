import discord
import os
import asyncio
import random
from webserver import alive
from discord.ext import commands
from discord.ext import tasks

PING_DELAY = 300
GAME = 'MONSTER HUNTER RISE'
INSULTS = [
    'TROGLODYTE', 'SMOOTHBRAIN', 'BITCH', 'SHITLORD', 'ASSHAT', 'CUM GUZZLER',
    'POOPY HEAD'
]

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
        count = 0
        for member in bot.get_all_members():
            if member.name == bot.user.name:
                continue

            if member.activities != None:
                for activity in member.activities:
                    if activity.name.upper().find(GAME) != -1:
                        title = f'EW {member} IS PLAYING {GAME}'
                        desc = f'{member.mention} GO TAKE A SHOWER YOU SMELLY {random.choice(INSULTS)}'
                        file = discord.File('./resources/shower.gif')
                        await channel.send(member.mention)
                        await channel.send(embed=discord.Embed(
                            title=title, description=desc, color=0xEE4B2B),
                                           file=file)
                        count = count + 1

        if count == 0:
            title = f'no one is playing {GAME.lower()}'
            desc = 'good'
            file = discord.File('./resources/good.jpg')
            await channel.send(embed=discord.Embed(title=title,
                                                   description=desc,
                                                   color=0x66ff00),
                               file=file)

        await asyncio.sleep(PING_DELAY)


def main():
    print('starting bot')
    alive()
    look_for_genshin_players.start()
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
