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
		title = msg[msg.index("{" + 1) : msg.index("}")].strip()
		desc = msg[msg.index("'" + 1) : msg.index("[")].strip()
		options = msg[msg.index("[" + 1) : msg.index("]")].split(",")
		for option in options:
			txt = option[[option.index("(") + 1] : option.index(":") - 1]
			emoji = option[[option.index(":")] : option.index(")")]
			option = [txt, emoji]

		tokens = {"title": title, "desc": desc, "options": options}
		return tokens
