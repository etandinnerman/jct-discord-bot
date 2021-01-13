import discord


class Poll:
	def __init__(self, msg):
		self.getTokens(msg.content)
		self.embed = self.getEmbed(msg)

	def getTokens(self, msg: str):
		self.options = msg.split("\n")
		self.options.pop(0)  # get rid of ++poll
		self.title = self.options.pop(0)
		# check that duration is a number
		if self.options[0].isnumeric():
			self.duration = int(self.options.pop(0))
		else:
			self.options.pop(0)
			self.duration = 3600
		self.emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

	def getEmbed(self, msg):
		embed = discord.Embed(title=self.title)
		embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
		for i in range(len(self.options)):
			embed.add_field(name=self.emojis[i], value=self.options[i], inline=True)
		return embed
