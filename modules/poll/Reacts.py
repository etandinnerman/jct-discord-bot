import discord
from modules.poll.cog import PollCog


class Reacts(PollCog):
	def __init__(self, msg, options):
		reactions = self.createReactions(msg, options)


	def createReactions(self, msg, options):
		reactions = []
		for option in options:
			re = discord.Reaction(message=msg, emoji=option[1])
			reactions.append(re)
		return reactions

	# functions for responding to interactions with reacts will also go in this class