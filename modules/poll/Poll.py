import discord
from modules.poll.cog import PollCog


class Poll(PollCog):
	def __init__(self, msg):
		tokens = self.getTokens(msg)
		embed = self.getEmbed(msg, tokens)

	def getEmbed(self, msg, tokens):
		embed = discord.Embed(title=tokens["title"], description=tokens["desc"])
		embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
		return embed

	def getTokens(self, msg: str):

		title = msg[msg.index("{" + 1) : msg.index("}")]
		title = title.strip()

		desc = msg[msg.index("'" + 1) : msg.index("[")]
		desc = desc.strip()

		options = msg[msg.index("[" + 1) : msg.index("]")].split(",")
		options = [option.strip() for option in options]

		tokens = {
			"title" : title,
			"desc" : desc,
			"options" : options
		}
		return tokens
