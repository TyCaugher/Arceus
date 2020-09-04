import discord, asyncio 
from discord.ext import commands 

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def game(self, ctx, *, role):
        """What game do you play?"""
        # Options: VG, TGC, POGO, Masters, etc
        user = ctx.message.author
        try:
            r = discord.utils.get(ctx.guild.roles, name=role)
            if r in user.roles:
                await user.remove_roles(r)
                await ctx.send("Removed {}".format(role))
            else:
                await user.add_roles(r)
                await ctx.send("Done!")
        except:
            await ctx.send("Invalid role selection")

def setup(bot):
    bot.add_cog(General(bot))
