from modules.poll.cog import PollCog


class Reacts(PollCog):
	def __init__(self, poll):
		reactions = self.getReactions(poll)


	def getReactions(self, poll):
		reactions = {}
		for option in poll.options:
			opt = option[: option.index(":")].strip()
			emoji = option[option.index(":") + 1 :].strip()
			reactions.update({opt: emoji})
		return reactions
