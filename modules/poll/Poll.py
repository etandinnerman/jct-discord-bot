import discord
from modules.poll.cog import PollCog


class Poll(PollCog):
    def __init__(self, msg):
        tokens = Poll.getTokens(self, msg)
        embed = Poll.getEmbed(self, msg, tokens)




    def getEmbed(self, msg, tokens):
        embed = discord.Embed(title=tokens[0], description=tokens[1])
        embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
        return embed



