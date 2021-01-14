import discord
from discord.ext import commands
from modules.poll.poll import Poll

# from modules.poll.reacts import Reacts


class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="poll")
	async def poll(self, ctx, *args):
		""" A command to create new user polls """

		# Create the Poll object
		poll = Poll(ctx.message)
		msg = await ctx.send(embed=poll.embed, delete_after=poll.duration)
		for i in range(len(poll.options)):
			await msg.add_reaction(poll.emojis[i])
		# delete the og message
		await ctx.message.delete()


def setup(bot):
	bot.add_cog(PollCog(bot))
