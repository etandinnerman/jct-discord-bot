class Poll(PollCog):
	def __init__(self, msg):

		tokens = getTokens(msg)
		embed = getEmbed(msg, tokens)

		reacts = tokens[3:]
		for i, react in reacts:
			emoji = ":" + str(i+1) + ":"
			await discord.Message.add_reaction(emoji)


	def getTokens(msg):
		tokens = msg.split("|")
		tokens = [token.strip() for token in tokens]
		return tokens

	
	def getEmbed(msg, tokens):
		embed = discord.Embed(title=tokens[0], description=tokens[1])
		embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
		return embed

		