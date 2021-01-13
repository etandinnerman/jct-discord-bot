def getTokens(self, msg: str):
	title = msg[msg.index("{") + 1 : msg.index("}")].strip()
	desc = msg[msg.index("'") + 1 : msg.index("[")].strip()
	options = msg[msg.index("[") + 1 : msg.index("]")].split(",")
	for option in options:
		txt = option[[option.index("(") + 1] : option.index(":") - 1].strip()
		emoji = option[[option.index(":")] : option.index(")")].strip()
		option = [txt, emoji]

	tokens = {"title": title, "desc": desc, "options": options}
	return tokens
