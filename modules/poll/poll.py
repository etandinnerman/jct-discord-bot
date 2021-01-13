import discord
from modules.poll.cog import PollCog


class Poll(PollCog):
	def __init__(self, msg, tokens):
		embed = self.getEmbed(msg, tokens)

	def getEmbed(self, msg, tokens):
		embed = discord.Embed(title=tokens["title"], description=tokens["desc"])
		embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
		for option in tokens.options:
			embed.add_field(name=option[0], value=option[1], inline=True)
		return embed
