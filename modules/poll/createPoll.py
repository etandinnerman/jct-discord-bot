def createPoll(msg: str):

	# TODO: Smarter text parsing, we CANNOT make this many assumptions about input
	# strip the command trigger from the message and split on "|" character
	tokens = msg.replace("~poll", "").split("|")

	# strip leading/trailing whitespace from each token
	tokens = [token.strip() for token in tokens]

	# this could be done inline in the embed() creation but I am saving them here for clarity and possible reuse
	poll_query = tokens[0]
	poll_desc = tokens[1]
	poll_options = [token for token in tokens[3:]]

	# the embed object will contain the formatted poll in the bot message
	poll_embed = discord.Embed(title=poll_query, description=poll_desc)
	poll_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	for i, option in poll_options:
		embed.add_field(name="", value=option, inline=false)
