import discord
from discord.ext import commands
from modules.poll import Poll, Reacts, getTokens


class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="poll")
	async def poll(self, ctx, *args):
		""" A command to create new user polls """

		# Tokenize the command string
		# Command String: ++poll {Title} 'Description' [ (Option :emoji:), (Option :emoji:), ... ]
		tokens = getTokens(ctx.message.content)

		# Create the Poll object
		poll = Poll(tokens)

		# Create the Reacts object
		reacts = Reacts(tokens.options, ctx.message)

		msg = await ctx.send(content=None, embed=poll.embed, delete_after=300, nonce=1)
		for react in reacts:
			await msg.add_reaction(react)


def setup(bot):
	bot.add_cog(PollCog(bot))
