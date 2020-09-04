import pokebase as pb 
from tinydb import TinyDB, Query
from discord.ext import commands
import discord, math

dex = TinyDB('cache/dex.json')
entry = Query()

class Pokemon(commands.Cog):
    """Pokemon lookup, info and more."""
    def __init__(self, bot):
        self.bot = bot 
    
    # A dex entry will consist of:
    # str Name, int id, list types, list abilities, dict base stats, dict evolutions & list evo lvls

    def dbCheck(self, name, db):
        """Check to see if a pokemon is cached in dex.json.  If so, return true."""
        e = db.get(entry.name == name)

        if e == None:
            return False
        else:
            return True

    def register(self, pkmn):
        """Cache a pkmn into the databse.  Take a pokeapi obj"""

        typing = [typ.type.name for typ in pkmn.types]
        abilities = [ab.ability.name for ab in pkmn.abilities]
        stats = {} 
        dexEntry = pkmn.species.flavor_text_entries[0].flavor_text
        total = 0
        
        for st in pkmn.stats:
            name = st.stat.name # Name of the stat
            base = st.base_stat # Base stat
            total += base # Add to the BST
            stats[name] = base

        stats['total'] = total
        typing = '/'.join(typing)

        return dex.insert({'name': pkmn.name,
                    'type': typing,
                    'id': pkmn.id,
                    'weight': pkmn.weight,
                    'height': pkmn.height,
                    'stats': stats,
                    'abilities': abilities})

    @commands.command()
    async def shiny(self, ctx, name):
        """Send the shiny version of the desired pokemon"""
        try:
            #await ctx.send(file=discord.File(r"sprites\front\shiny\{}.gif".format(name)))
            await ctx.send('https://play.pokemonshowdown.com/sprites/ani-shiny/{}.gif'.format(name.lower()))
        except:
            await ctx.send("Pokemon not found, typo perhaps?")       

    @commands.command()
    async def info(self, ctx, name):
        """Grab a summary of a pokemon like you would see in-game"""
       # embed = discord.Embed(color=discord.Color.dark_red)

        def buildStats(stats):
            """takes a dict(), Build a visually pleasing display of the stats"""
            statbar = []
            for stat in stats:
                val = stats[stat]
                val /= 20
                math.floor(val)
                if val < 3:
                    icon = ':brown_square:'
                if 3 <= val <= 5:
                    icon = ':orange_square:'
                if val > 5:
                    icon = ':green_square:'
                bar = int(val)*icon
                statbar.append(bar)

            hp = "**HP**:\n{}, **{}**\n".format(statbar[0], stats['hp'])
            atk = "**ATK**:\n{} **{}**\n".format(statbar[1], stats['attack'])
            df = "**DEF**:\n{} {}\n".format(statbar[2], stats['defense'])
            spatk = "**SP.ATK**:\n{} {}\n".format(statbar[3], stats['special-attack'])
            spdf = "**SP.DEF**:\n{} {}\n".format(statbar[4], stats['special-defense'])
            spd = "**SPD**:\n{} {}\n".format(statbar[5], stats['speed'])
            t = "**Total**: {}".format(stats["total"])

            return hp + atk + df + spatk + spdf + spd + t

        name = name.lower()
        
        inDex = self.dbCheck(name, dex) # Do a check to see if its in the cache
        #If at all possible, do NOT send an API req and use cache.  API is slow af
        if inDex:
            summary = dex.get(entry.name == name)
        else:
            async with ctx.channel.typing(): # Send typing because this takes long af
                #try:
                pkmn = pb.pokemon(name) # Quick lookup of the pokemon
                self.register(pkmn)
                summary = dex.get(entry.name == name)
                #except:

        statblock = buildStats(summary['stats'])
        height = summary['height'] / 3.048
        weight = summary['weight'] / 4.536

        #img = discord.File(r'sprites\front\normal\{}.gif'.format(name), filename="{name}.gif")

        embed = discord.Embed(title=summary['name'].title(), color=0x00ff00, url='https://bulbapedia.bulbagarden.net/wiki/{}_(Pok%C3%A9mon)'.format(summary['name'].lower()))
        embed.add_field(name='Type', value=summary['type'].title(), inline=True)
        embed.add_field(name='Weight', value="{:.1f} lbs".format(weight), inline=True)
        embed.add_field(name='Height', value="{:.1f} ft".format(height), inline=True)
        embed.add_field(name='Stats', value=statblock, inline=False)
        embed.add_field(name='Abilties', value=' | '.join(summary['abilities']).title(), inline=True)
        #embed.set_thumbnail(url='attachment://{}.gif.'.format(name))
        embed.set_thumbnail(url='https://play.pokemonshowdown.com/sprites/ani/'+name.lower()+'.gif')

        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    # THIS COMMAND IS ABSOLUTELY FUCKED WIP
    async def movelist(self, ctx, name):
        """List a pokemon's moves ! THIS COMMAND IS FUCKED AND DOESN'T WORK !"""
        movedex = TinyDB('cache/moves.json')
        # +======================+
        # |    Move    | Typ  Po |
        # +======================+
        # | Aerial Ace | AT | 60 |
        # +----------------------+

        inDex = self.dbCheck(name, movedex)
        if inDex:
            moves = movedex.get(entry.name == name)
        else:
            pkmn = pb.pokemon(name)
            mvlist = [mv.move.name for mv in pkmn.moves]
            dmgtypes = [mv.move.damage_class.name for mv in pkmn.moves]
            pwr = [mv.move.power for mv in pkmn.moves]

            movedex.insert({'name': name,
                           'moves': mvlist,
                           'dmgtypes': dmgtypes,
                           'power': pwr})

            moves = movedex.get(entry.name == name)

        header = "+======================+\n|    Move    | Typ  Po |\n+======================+"
        divider = "+----------------------+"
        prettyTable = []

        prettyTable.append(header)
        for i in range(len(moves["name"])):
            n = moves["name"][i]            
            if len(n) > 10:
                n = n[0:10]
            t = moves["dmgtypes"][i]
            t = t[0:2]
            p = moves["power"][i]
            prettyTable.append("| {} | {} | {} |".format(n, t, p))
            prettyTable.append(divider)

        table = '\n'.join(prettyTable)
        table = "```markdown {}```".format(table)

        await ctx.send(table)


def setup(bot):
    bot.add_cog(Pokemon(bot))
        
