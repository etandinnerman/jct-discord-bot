import discord
from discord.ext import commands
from modules.poll,createPoll import createPoll


class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="poll")
	async def poll(self, ctx, *args):
		""" A command to create new user polls """

		poll = createPoll(ctx.message.content)


def setup(bot):
	bot.add_cog(PollCog(bot))
