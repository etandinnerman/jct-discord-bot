import os
import re
import csv
from datetime import datetime
from itertools import product
from typing import Dict, Iterable, Mapping, Optional, Tuple
import dateparser
import asyncio
import discord
from discord.ext import commands
from modules.error.friendly_error import FriendlyError

class IdNotFoundError(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)


def get_discord_obj(iterable, label: str):
	return discord.utils.get(iterable, id=get_id(label))


def get_id(label: str) -> int:
	"""gets the id of an object that has the given label in the CSV file"""
	with open(os.path.join("utils", "ids.csv")) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		for row in csv_reader:
			if row[0] == label:
				return int(row[1])
		raise IdNotFoundError(f"There is not ID labeled {label} in ids.csv")


def remove_tabs(string: str) -> str:
	"""removed up to limit_per_line (default infinitely many) tabs from the beginning of each line of string"""
	return re.sub(r"\n\t*", "\n", string).strip()


def blockquote(string: str) -> str:
	"""Add blockquotes to a string"""
	# inserts > at the start of string and after new lines
	# as long as it is not at the end of the string
	return re.sub(r"(^|\n)(?!$)", r"\1> ", string.strip())


def embed_success(
	title: str,
	description: str = None,
	colour: discord.Colour = discord.Colour.green(),
) -> discord.Embed:
	"""Embed a success message and an optional description"""
	embed = discord.Embed(title=title, colour=colour)
	if description:
		embed.description = description
	return embed


def ordinal(n: int):
	return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4])


def decode_mention(mention: str) -> Tuple[Optional[str], Optional[int]]:
	"""returns whether mention is a member mention or a channel mention (or neither) as well as the id of the mentioned object"""
	match = re.search(r"<(#|@)!?(\d+)>", mention)
	if match is None:
		return None, None
	else:
		groups = match.groups()
		return "channel" if groups[0] == "#" else "member", groups[1]


def is_email(email: str) -> bool:
	return bool(re.search(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email))


def build_aliases(
	name: str,
	prefix: Iterable[str],
	suffix: Iterable[str],
	more_aliases: Iterable[str] = (),
	include_dots: bool = True,
) -> Mapping:
	dots = ("", ".") if include_dots else ("")
	return {
		"name": name,
		"aliases": list(more_aliases)
		+ [a + b + c for a, b, c in product(prefix, dots, suffix) if a + b + c != name],
	}


def parse_date(
	date_str: str,
	from_tz: str = None,
	to_tz: str = None,
	future: bool = None,
	base: datetime = None,
	settings: Dict[str, str] = {},
) -> Optional[datetime]:
	"""Returns datetime object for given date string
	Arguments:
	<date_str>: date string to parse
	[from_tz]: string representing the timezone to interpret the date as (ex. "Asia/Jerusalem")
	[to_tz]: string representing the timezone to return the date in (ex. "Asia/Jerusalem")
	[future]: set to true to prefer dates from the future when parsing
	[base]: datetime representing where dates should be parsed relative to
	[settings]: dict of additional settings for dateparser.parse()
	"""
	if date_str is None:
		return None
	settings = {
		**settings,
		**({"TIMEZONE": from_tz} if from_tz else {}),
		**({"TO_TIMEZONE": to_tz} if to_tz else {}),
		**({"PREFER_DATES_FROM": "future"} if future else {}),
		**({"RELATIVE_BASE": base.replace(tzinfo=None)} if base else {}),
	}
	return dateparser.parse(date_str, settings=settings)


def format_date(
	date: datetime, base: datetime = datetime.now(), all_day: bool = False
) -> str:
	"""Convert dates to a specified format
	Arguments:
	<date>: The date to format
	[base]: When the date or time matches the info from base, it will be skipped.
			This helps avoid repeated info when formatting time ranges.
	[all_day]: If set to true, the time of the day will not be included
	"""
	date_format = ""
	# include the date if the date is different from the base
	if date.date() != base.date():
		# %a = Weekday (ex. "Mon"), %d = Day (ex. "01"), %b = Month (ex. "Sep")
		date_format = "%a %d %b"
		# include the year if the date is in a different year
		if date.year != base.year:
			# %Y = Year (ex. "2021")
			date_format += " %Y"
	# include the time if it is not an all day event and not the same as the base
	if not all_day and date != base:
		# %I = Hours (12-hour clock), %M = Minutes, %p = AM or PM
		date_format += " %I:%M %p"
	# format the date and remove leading zeros and trailing spaces
	return date.strftime(date_format).replace(" 0", " ").strip()


async def wait_for_reaction(
	bot: commands.Bot,
	message: discord.Message,
	emoji_list: Iterable[str],
	allowed_users: Iterable[discord.Member] = None,
	timeout: int = 60,
) -> int:
	"""Add reactions to message and wait for user to react with one.
	Returns the index of the selected emoji (integer in range 0 to len(emoji_list) - 1)
	
	Arguments:
	<bot>: str - the bot user
	<message>: str - the message to apply reactions to
	<emoji_list>: Iterable[str] - list of emojis as strings to add as reactions
	[allowed_users]: Iterable[discord.Member] - if specified, only reactions from these users are accepted
	[timeout]: int - number of seconds to wait before timing out
	"""

	def validate_reaction(reaction: discord.Reaction, user: discord.Member) -> bool:
		"""Validates that:
			- The reaction is on the message currently being checked
			- The emoji is one of the emojis on the list
			- The reaction is not a reaction by the bot
			- The user who reacted is one of the allowed users
		"""
		return (
			reaction.message == message
			and str(reaction.emoji) in emoji_list
			and user != bot.user
			and (allowed_users is None or user in allowed_users)
		)

	# add reactions to the message
	for emoji in emoji_list:
		await message.add_reaction(emoji)

	try:
		# wait for reaction (returns reaction and user)
		reaction, _ = await bot.wait_for("reaction_add", check=validate_reaction, timeout=timeout)
	except asyncio.TimeoutError as error:
		# clear reactions
		await message.clear_reactions()
		# raise timeout error as friendly error
		raise FriendlyError(
			f"You did not react within {timeout} seconds",
			message.channel,
			allowed_users[0] if len(allowed_users) == 1 else None,
			error,
		)
	else:
		# clear reactions
		await message.clear_reactions()
		# return the index of the emoji selection
		return emoji_list.index(str(reaction.emoji))
