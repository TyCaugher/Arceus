import logging
import discord
import sys
from discord.ext import commands
from configparser import ConfigParser
#Pokemon club management bot 2020.
#See feature plans txt for the intended use.

config = ConfigParser()
config.read('config.ini')
token = config.get('main', 'token')

bot = commands.Bot(command_prefix='~')
startup = ['pokebase', 'trainercards']


# Startup event
@bot.event
async def on_ready():
    """When the bot is ready and load respective startup cogs"""
    print('\n--------------------------------------')
    print('Logged in as')
    print(bot.user.name)

    # Load cogs
    for ext in startup:
        try:
            bot.load_extension("cogs.{}".format(ext))

        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extention {}\n{}'.format(ext, exc))
    # Set discord presence
    game = discord.Game("with mega stones.")
    await bot.change_presence(status=discord.Status.idle, activity=game)

# On user join.
@bot.event
async def on_member_join(member):
   await bot.get_channel(356836239011479553).send(f" Welcome {member.name} to the Discord of Tech Pokemon.  Make sure to stop by #rules and #announcements.  Enjoy your stay!")


@bot.command()
async def ping(ctx):
    """pong"""
    await ctx.send('pong')


@bot.command()
async def reload(ctx, ext_name: str):
    """Reload a cog"""
    ext_name = 'cogs.' + ext_name
    bot.unload_extension(ext_name)
    bot.load_extension(ext_name)

    await ctx.send("{} reloaded.".format(ext_name))

@bot.command()
async def load(ctx, ext_name: str):
    ext_name = 'cogs.' + ext_name
    bot.load_extension(ext_name)

    await ctx.send('{} loaded'.format(ext_name))

@bot.command()
async def exit(ctx):
    sys.exit("Recieved exit cmd")
    await ctx.send("Exiting")

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot.run(token)
