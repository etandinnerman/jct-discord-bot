import random
import discord
from discord.ext import commands
import utils.utils as utils


class Assigner:
	"""
	Assigns users their roles and name, and welcomes them once done.
	"""

	def __init__(self, guild: discord.Guild):
		self.unassigned_role = guild.get_role(utils.get_id("UNASSIGNED_ROLE"))
		self.student_role = guild.get_role(utils.get_id("STUDENT_ROLE"))
		self.welcome_channel = guild.get_channel(utils.get_id("OFF_TOPIC_CHANNEL"))

	async def assign(self, member: discord.Member, name: str, campus: str, year: int):
		if self.unassigned_role in member.roles:
			await member.edit(nick=name)
			await self.__add_role(member, campus, year)
			await member.add_roles(self.student_role)
			await member.remove_roles(self.unassigned_role)
			print(f"Removed Unassigned from {member} and added Student")
			await self.server_welcome(member)

	async def __add_role(self, member: discord.Member, campus: str, year: int):
		"""adds the right role to the user that used the command"""
		# formatting role for csv file, eg LEV_YEAR_1_ROLE
		role_label = f"{campus.upper()}_YEAR_{year}_ROLE"
		class_role = utils.get_discord_obj(member.guild.roles, role_label)

		# check if the role was found
		if class_role == None:
			raise ValueError(f"Could not find the role for {role_label}.")

		await member.add_roles(class_role)
		print(f"Gave {class_role.name} to {member.display_name}")

	async def server_welcome(self, member: discord.Member):
		# Sets the channel to the welcome channel and sends a message to it
		welcome_emojis = ["🎉", "👋", "🌊", "🔥", "😎", "👏", "🎊", "🥳", "🙌", "✨", "⚡"]
		random_emoji = random.choice(welcome_emojis)
		nth = utils.ordinal(len(self.student_role.members))
		await self.welcome_channel.send(
			f"Everyone welcome our {nth} student {member.mention} to the"
			f" server! Welcome! {random_emoji}"
		)
