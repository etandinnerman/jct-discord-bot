import discord
from discord.ext import commands
from modules.poll import Poll


class PollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def poll(self, ctx, *args):
        """ A command to create new user polls """
        """ ++poll Title | Desc | Option 1 | Option 2 | ... | Option n """
        poll = Poll(ctx.message.content, args)
        await ctx.send(content=None, embed=poll.embed, delete_after=300, nonce=1)



def setup(bot):
    bot.add_cog(PollCog(bot))
