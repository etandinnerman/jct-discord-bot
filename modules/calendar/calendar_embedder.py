from datetime import datetime
from typing import Iterable, Dict
import discord
from utils.utils import parse_date


class CalendarEmbedder:
	def __init__(self):
		self.timezone = "Asia/Jerusalem"

	def embed_event_list(
		self,
		title: str,
		events: Iterable[dict],
		description: str = "",
		colour: discord.Colour = discord.Colour.green(),
	) -> discord.Embed:
		"""Generates an embed with event summaries, links, and dates for each event in the given list"""
		embed = discord.Embed(title=title, colour=colour)
		# set initial description if available
		embed.description = "" if description == "" else f"{description}\n\n"
		if not events:
			embed.description += "No events found"
		else:
			# add events to embed
			event_details = map(self.__get_formatted_event_details, events)
			embed.description += "\n".join(event_details)
		embed.set_footer(text=self.__get_footer_text())
		return embed

	def embed_link(
		self,
		title: str,
		links: Dict[str, str],
		colour: discord.Colour = discord.Colour.green(),
	) -> discord.Embed:
		"""Embed a list of links given a mapping of link text to urls"""
		embed = discord.Embed(title=title, colour=colour)
		# add links to embed
		description = (f"\n**[{text}]({url})**" for text, url in links.items())
		embed.description = "\n".join(description)
		return embed

	def embed_event(
		self,
		title: str,
		event: Dict[str, str],
		colour: discord.Colour = discord.Colour.green(),
	) -> discord.Embed:
		"""Embed an event with the summary, link, and dates"""
		embed = discord.Embed(title=title, colour=colour)
		# add overview of event to the embed
		embed.description = self.__get_formatted_event_details(event)
		embed.set_footer(text=self.__get_footer_text())
		return embed

	def __get_formatted_event_details(self, event: Dict[str, str]) -> str:
		"""Format event as a markdown linked summary and the dates below"""
		return (
			f"**[{event.get('summary')}]({event.get('htmlLink')})**\n"
			f"{self.__get_formatted_date_range(event)}\n"
		)

	def __get_formatted_date_range(self, event: Dict[str, str]) -> str:
		"""Extract dates from event and convert to readable format"""
		start = event["start"].get("dateTime", event["start"].get("date"))
		end = event["end"].get("dateTime", event["end"].get("date"))
		start_date = parse_date(start, tz=self.timezone)
		end_date = parse_date(end, tz=self.timezone)
		# all day event
		if "date" in event["start"]:
			return f"{self.__format_date(start_date, all_day=True)} - All day"
		# start and end time
		formatted_start_date = self.__format_date(start_date)
		formatted_end_date = self.__format_date(end_date, base=start_date)
		return formatted_start_date + (
			f" - {formatted_end_date}" if formatted_end_date else ""
		)

	def __format_date(
		self, date: datetime, base: datetime = datetime.now(), all_day: bool = False
	) -> str:
		"""Convert dates to a specified format"""
		format = ""
		# if the date is same as the base, don't include the date
		if date.strftime("%d %b") != base.strftime("%d %b"):
			format = "%a %d %b"
			# if the date is not in the same year as base
			if date.year != base.year:
				format += " %Y"
		# if all day, and the time is not the same as the base, return the time
		if not all_day and date.strftime("%d%b%I:%M%p") != base.strftime("%d%b%I:%M%p"):
			format += " %I:%M %p"
		return date.strftime(format).replace(" 0", " ").strip()

	def __get_footer_text(self):
		"""Return text about timezone to display at end of embeds with dates"""
		return f"Times are shown for {self.timezone}"
