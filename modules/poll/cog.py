import discord
from discord.ext import commands


class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		reacts = [
			# TODO: Figure out this emoji crap and build a list encodings for numerals 0-25
		]

	@commands.command(name="poll")
	async def poll(self, ctx, *args):
		"""
		A command to create new user polls
		[ Title | Description | inline (True/False)] | Options (2-26) ]
		"""

		# strip the command trigger from the message
		msg = ctx.message.content.replace("~poll", "")

		# split the command into args and remove leading/trailing whitespace
		sentence = msg.split("|")
		sentence = [word.strip() for word in sentence]

		# TODO: Smarter text parsing, we CANNOT make this many assumptions about input
		# 		Right now the focus is on building a minimum viable product

		# initialize the embed and assign a few attributes we'll need later
		embed = discord.Embed(title=sentence[0], description=sentence[1])
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		inline = sentence[2]

		for word in sentence[3:]:
			embed.add_field(value="", name=word, inline=inline)

		for i, field in embed.fields:
			field.value = await add_reaction(self.reacts[i])


def setup(bot):
	bot.add_cog(PollCog(bot))
