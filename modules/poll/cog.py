import discord
from discord.ext import commands
from modules.poll.poll import Poll

# from modules.poll.reacts import Reacts


class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.polls = {}

	@commands.command(name="poll")
	async def poll(self, ctx, *args):
		""" A command to create new user polls """
		# Create the Poll object
		poll = Poll(ctx.message)
		self.polls[ctx.message] = poll
		self.msg = await ctx.send(embed=poll.embed, delete_after=poll.duration)
		for i in range(len(poll.options)):
			await self.msg.add_reaction(poll.emojis[i])
		# delete the og message
		await ctx.message.delete()

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
		if reaction.message in self.polls:
			self.polls[reaction.message].vote(reaction, member)

	@commands.Cog.listener()
	async def on_reaction_remove(self, reaction: discord.Reaction, member: discord.Member):
		if reaction.message in self.polls:
			self.polls[reaction.message].unvote(reaction, member)

def setup(bot):
	bot.add_cog(PollCog(bot))
