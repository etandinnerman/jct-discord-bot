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
		[ Query | Description | Options (2-26) ]
		"""

		# strip the command trigger from the message
		msg = ctx.message.content.replace("~poll", "")

		# TODO: Smarter text parsing, we CANNOT make this many assumptions about input
		# 		Right now the focus is on building a minimum viable product
		
		# split the command into args and remove leading/trailing whitespace
		sentence = msg.split("|")
		sentence = [word.strip() for word in sentence]
		poll_query = sentence[0]
		poll_desc = sentence[1]
		poll_options = [
			sentence[i] for i in range(2, len(sentence))
		]  # error related to list comprehension, cannot figure

		# the embed will contain the formatted poll
		poll_embed = discord.Embed(title=poll_query, description=poll_desc)
		poll_embed.set_author(
			name=ctx.author.display_name, icon_url=ctx.author.avatar_url
		)
		for i, option in poll_options:
			embed.add_field(
				name="", value=":regional_indicator_" + i + ":", inline=True
			)

		await send(content=None, embed=embed)


def setup(bot):
	bot.add_cog(PollCog(bot))
