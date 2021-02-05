from typing import Iterable, Dict
import discord
import dateparser


class CalendarEmbedder:
	def __init__(self):
		self.default_time_zone = "Asia/Jerusalem"

	def embed_event_list(self, title: str, events: Iterable[dict]) -> discord.Embed:
		"""Generates an embed with event summaries, links, and dates for each event in the given list"""
		embed = discord.Embed(title=title, colour=discord.Colour.green())
		if not events:
			embed.description = "No events found"
		else:
			# add events to embed
			event_details = map(self.__get_formatted_event_details, events)
			embed.description = "\n".join(event_details)
		embed.set_footer(text=self.__get_footer_text())
		return embed

	def embed_link(self, title: str, links: Dict[str, str]) -> discord.Embed:
		"""Embed a list of links given a mapping of link text to urls"""
		embed = discord.Embed(title=title, colour=discord.Colour.green())
		# add links to embed
		description = (f"\n**[{text}]({url})**" for text, url in links.items())
		embed.description = "\n".join(description)
		return embed

	def embed_event(self, title: str, event: Dict[str, str]) -> discord.Embed:
		"""Embed an event with the summary, link, and dates"""
		embed = discord.Embed(title=title, colour=discord.Colour.green())
		# add overview of event to the embed
		embed.description = self.__get_formatted_event_details(event)
		embed.set_footer(text=self.__get_footer_text())
		return embed

	def embed_success(self, title: str, description: str = None) -> discord.Embed:
		"""Embed a success message and an optional description"""
		embed = discord.Embed(title=title, colour=discord.Colour.green())
		if description:
			embed.description = description
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
		return f"{self.__format_date(start)} - {self.__format_date(end)}"

	def __format_date(self, date_str: str) -> str:
		"""Convert dates to format: 'Jan 1 2021 1:23 AM'"""
		date = dateparser.parse(
			date_str, settings={"TO_TIMEZONE": self.default_time_zone}
		)
		return date.strftime("%b %d %Y %I:%M %p").replace(" 0", " ")

	def __get_footer_text(self):
		"""Return text about timezone to display at end of embeds with dates"""
		return f"Times are shown for {self.default_time_zone}"