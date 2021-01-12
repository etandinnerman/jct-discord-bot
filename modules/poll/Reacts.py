# import discord
# from modules.poll.cog import PollCog


from modules.poll.cog import PollCog


class Reacts(PollCog):
    def __init__(self, poll):
        users = Reacts.getUsers(self, uid)
        reactions = Reacts.getReacts(self, poll)


    def getReacts(self, poll):



