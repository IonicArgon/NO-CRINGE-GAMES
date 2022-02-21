import discord
import os
import asyncio
import random
import json
import datetime
from webserver import alive
from discord.ext import commands
from discord.ext import tasks

PING_DELAY = 0
GAMES = []
INSULTS = []
IMAGE_URLS = []
MEMBERS = {}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!ngi'),
                   discription='NO GENSHIN IMPACT',
                   intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('logged on as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name='NO CRINGE GAMES'))


@tasks.loop(seconds=10)
async def load_json():
    global PING_DELAY
    global GAMES
    global INSULTS
    global IMAGE_URLS

    await bot.wait_until_ready()

    print(f'updating config from json @ {datetime.datetime.now()} UTC')

    with open('./src/config.json', 'r') as file:
        data = json.load(file)
        PING_DELAY = data['ping_delay']
        GAMES = data['games']
        INSULTS = data['insults']
        IMAGE_URLS = data['image_urls']

    print(f'ping delay: {PING_DELAY}\n' + f'games:\n \t{GAMES}\n' +
          f'insults:\n \t{INSULTS}\n' + f'image urls:\n \t{IMAGE_URLS}\n')


@tasks.loop(seconds=60)
async def look_for_genshin_players():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(os.getenv('ANNOUNCEMENTS')))
    footer_text = 'bot made by Extro#7573'

    while not bot.is_closed():
        count = 0
        time = datetime.datetime.now()

        print(f'tracked members:\n {MEMBERS}')

        for member in bot.get_all_members():
            if member.name == bot.user.name:
                continue

            if member.name in MEMBERS:
                for activity in member.activities:
                    if activity.name is None:
                        continue
                    elif activity.name.upper() == MEMBERS[member.name]:
                        count += 1
                        continue
                    elif activity.type == discord.ActivityType.custom:
                        continue
                    else:
                        count -= 1
                        del MEMBERS[member.name]
                continue

            if member.activities is not None:
                for activity in member.activities:
                    if activity.name is None:
                        continue
                    if any(substring in activity.name.upper()
                           for substring in GAMES):
                        title = f'EW {member} IS PLAYING {activity.name.upper()}'
                        desc = f'{member.mention} GO TAKE A SHOWER YOU SMELLY {random.choice(INSULTS)}\nTimestamp: {time} UTC'
                        await channel.send(f'{member.mention}')
                        await channel.send(embed=discord.Embed(
                            title=title, description=desc,
                            color=0xEE4B2B).set_image(
                                url=IMAGE_URLS[0]).set_footer(text=footer_text)
                                           )
                        MEMBERS[member.name] = activity.name.upper()
                        count += 1

        print(f'cringe member count: {count}')

        if count == 0:
            title = 'no one is playing cringe games'
            desc = f'good\nTimestamp: {time} UTC'
            await channel.send(embed=discord.Embed(
                title=title, description=desc, color=0x66ff00).set_image(
                    url=IMAGE_URLS[1]).set_footer(text=footer_text))

        await asyncio.sleep(PING_DELAY)


def main():
    print('starting bot')
    alive()
    load_json.start()
    look_for_genshin_players.start()
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
