import discord, tinydb, asyncio
from discord.ext import commands 
from tinydb import Query

db_events = TinyDB('cache/events.json')

class Event:
    def __init__(self, title, date, desc)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    def messageInput(self, prompt, ctx):
        try:
            await asyncio.sleep(0.5)
            await ctx.send("Please give a {}:".format(prompt))
            msg = await self.bot.wait_for('message', timeout=60.0)
            #print(msg)
            #print(msg.content + "----------------\n\n\n\n\n")
        except asyncio.TimeoutError:
            await ctx.send("You took too long, cancelling.")
        else:
            #Return the msg
            if msg == "None":
                return None
            return msg

    @commands.group()
    async def event(self, ctx):
        """Event command category"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid event command")

    @event.command()
    @commands.has_permissions(administrator=True)
    async def create(self, ctx, *, name):

        """Create a new event"""
        # Events will take several details
        # Title
        # When: MM/DD/YY
        # Where: if empty, default to club location
        # Description: any deets
        # Format (Optional)
        # Prizes (Optional)

