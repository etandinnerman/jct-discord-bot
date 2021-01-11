from modules.role_tag.role import Role
from modules.role_tag.member import Member
from discord.ext import commands
import discord


class RoleTagsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_update(self, before: discord.Member, after: discord.Member):
		if before.roles != after.roles:
			before = Member(before)
			after = Member(after)
			if before.tags() != after.tags():
				await after.apply_tags()
				print(
					"Renamed",
					before.inner_member.display_name,
					"to",
					after.inner_member.display_name,
				)

	@commands.Cog.listener()
	async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
		before = Role(before)
		after = Role(after)
		if before.tag != after.tag:
			print(before.inner_role.name, "changed to", after.inner_role.name)
			for member in after.inner_role.members:
				await Member(member).apply_tags()


def setup(bot):
	bot.add_cog(RoleTagsCog(bot))