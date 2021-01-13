import discord
from modules.poll.cog import PollCog


class Reacts(PollCog):
	def __init__(self, options, msg):
		reactions = self.createReactions(options, msg)


	def createReactions(self, options, msg):
		reactions = []
		for option in options:
			re = discord.Reaction(emoji=option[1], message=msg)
			reactions.append(re)
		return reactions

	# functions for responding to interactions with reacts will also go in this class