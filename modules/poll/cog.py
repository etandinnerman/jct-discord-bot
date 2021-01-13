import discord
from discord.ext import commands
from modules.poll import Poll, Reacts


class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="poll")
	async def poll(self, ctx, *args):
		""" 
		A command to create new user polls
		Command Format: ++poll {Title} 'Description' [(Option :emoji:), (Option :emoji:), ... ]
		"""

		poll = Poll(ctx.message.content)
		reacts = Reacts(poll.tokens.options)

		# await ctx.send(content=None, embed=poll.embed, delete_after=300, nonce=1)


def setup(bot):
	bot.add_cog(PollCog(bot))
