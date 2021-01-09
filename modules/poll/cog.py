from discord.ext import commands


class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="poll")
	async def poll(self, ctx, *args):
		"""A command to create new user polls"""

		msg = ctx.message.content.replace('~poll', '')
		sentence = msg.split('|')
		print(sentence)


def setup(bot):
	bot.add_cog(PollCog(bot))
