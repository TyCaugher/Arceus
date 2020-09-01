import discord, asyncio
from tinydb import TinyDB, Query
from discord.ext import commands
from tinydb.queries import where

# Handles all of the trainer card functions including info, 

cards = TinyDB('cache/cards.json')
Trainer = Query()

class TrainerCards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cardcheck(self, item):
        item = item.lower()
        # This should return a dictionary
        cardField = cards.contains(Trainer.card == item)
        print(cardField)

        return cardField

    def itemFind(self, user):
        """Return a dict of the trainer's info"""
        items = cards.get(Trainer.name == user)
        if items == None:
            return None
        else:
            return items


    @commands.group()
    async def card(self, ctx):
        """Creates the group for the card commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid card command")


    @card.command()
    async def register(self, ctx):
        """First time setup"""

        # In the future, I want to make this save the color of the discord nicknmame too for great uniqueness n shit

        name = ctx.message.author.name.lower() # The name of the discord user calling the cmd
        if cards.get(Trainer.name == name) == None: # If their name is not found in the db
            cards.insert({'name': name, 
                          'card': {}})
            await ctx.send("{}, you have been issued a trainer card!  Type ~card help for available actions.".format(name))
        else:
            await ctx.send("You have already registered!")


    @card.command()
    async def add(self, ctx, *, field):
        """Add information to your card ~card add switch fc"""

        #def check(m):
       #     return m.channel == channel

        name = ctx.message.author.name.lower()
        c_info = cards.get(Trainer.name == name) #Return the dict of info
        # {'name': 'kroren', 'card': {}}
        # To edit card, we need
        # c_info['card'][field] = desired info
        # then, upsert
        # cards.upsert(c_info, Trainer.name = name)

        field = field.lower()
        if self.cardcheck(field):
            await ctx.send("{field} already exists on your trainer card!")
        else:
            try:
                await asyncio.sleep(0.5)
                await ctx.send("Please type the details of your entry")
                msg = await self.bot.wait_for('message', timeout=60.0)
                #print(msg)
                #print(msg.content + "----------------\n\n\n\n\n")
            except asyncio.TimeoutError:
                await ctx.send("You took too long, cancelling.")
            else:
                # This is probably a bad way to handle the data, but who fucking cares at this rate
                c_info['card'][field] = msg.content
                #print("\n\n\n" + c_info + "\n\n\n")
                cards.upsert(c_info, Trainer.name == name)
                await ctx.send("Added {}: {} to your trainer card!".format(field.title(), msg.content))

    @card.command()
    async def show(self, ctx, user: discord.Member=None): # discord.Member means that it must be a mention
        """Show your own trainer card, or somebody else's"""
        # Create an embed and set it up so it won't need to be done in the main code.
        if user == None: # If no uesr is specified, use the sender
            user = ctx.message.author
            color = user.color.value
            user = user.name
            # lmao fuckin reassignments im so retard
        else:
            color = user.color.value
            user = user.name
            

        cardInfo = cards.get(Trainer.name == user.lower())
        print(cardInfo)

        c_embed = discord.Embed(color=color)

        for item in cardInfo["card"]: # Iterate through the nested dict of card (custom details)
            c_embed.add_field(name=item.title(), value=cardInfo["card"][item])

        c_embed.set_author(name=cardInfo["name"].title(), icon_url=ctx.message.author.avatar_url)
        c_embed.set_footer(text="2020 Tech Pokemon ID")

        await ctx.send(embed=c_embed)

    @card.command()
    async def edit(self, ctx, field):
        """Edit a field"""

        field = field.lower()
        user = ctx.message.author.name.lower()

        items = self.itemFind(user)

        # this shit is wip and im too tired to finish it right now

    @card.command()
    async def delete(self, ctx, field):
        """Delete information from your card"""
        field = field.lower()
        user = ctx.message.author.name.lower()

        items = cards.get(Trainer.name == user)
        # this is utterly fucking stupid and inefficient but i couldnt care anymore
        try:
            del items['card'][field]
            items = items['card']

            cards.update({'card': items}, Trainer.name == user)
            await ctx.send("Deleted {} from your trainer card".format(field))
        except:
            await ctx.send("Unable to find " + field + " on your trainer card")

    
    # All admin commands will be below

def setup(bot):
    bot.add_cog(TrainerCards(bot))
