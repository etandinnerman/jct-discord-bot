import os
import config
from discord.ext import commands
from .calendar import Calendar
from .calendar_embedder import CalendarEmbedder
from .calendar_finder import CalendarFinder
from utils.sql_fetcher import SqlFetcher
from .class_role_error import ClassRoleError
from .class_parse_error import ClassParseError
from modules.error.friendly_error import FriendlyError
from utils.utils import is_email, build_aliases


class CalendarCog(commands.Cog, name="Calendar"):
	"""Display and update Google Calendar events"""

	def __init__(self, bot):
		self.bot = bot
		self.calendar = Calendar()
		self.calendar_embedder = CalendarEmbedder()
		self.sql_fetcher = SqlFetcher(os.path.join("modules", "calendar", "queries"))
		self.finder = CalendarFinder(config.conn, self.sql_fetcher)

	@commands.command(
		**build_aliases(
			name="calendar.links",
			prefix=("calendar", "events", "event"),
			suffix=("link", "links"),
		)
	)
	async def calendar_links(self, ctx):
		"""
		Get the links to add or view the calendar

		Usage:
		```
		++calendar.links
		```
		"""
		class_roles = self.finder.get_class_roles(ctx.author)
		for grad_year, campus in class_roles:
			calendar_id = self.finder.get_calendar_id(grad_year, campus)
			links = self.calendar.get_links(calendar_id)
			embed = self.calendar_embedder.embed_link(
				f"Calendar Links for {campus} {grad_year}", links
			)
			await ctx.send(embed=embed)

	@commands.command(
		**build_aliases(
			name="events.list",
			prefix=("calendar", "events", "event"),
			suffix=("upcoming", "list", "events"),
			more_aliases=("upcoming", "events"),
		)
	)
	async def events_list(self, ctx, max_results: int = 5):
		"""
		Display upcoming events from the Google Calendar

		Usage:
		```
		++events.list [max_results]
		```
		Arguments:
		**[max_results]**: The maximum number of events to display
		"""
		class_roles = self.finder.get_class_roles(ctx.author)
		for grad_year, campus in class_roles:
			calendar_id = self.finder.get_calendar_id(grad_year, campus)
			events = self.calendar.fetch_upcoming(calendar_id, max_results)
			embed = self.calendar_embedder.embed_event_list(
				f"Upcoming Events for {campus} {grad_year}", events
			)
			await ctx.send(embed=embed)

	@commands.command(
		**build_aliases(
			name="events.add",
			prefix=("calendar", "events", "event"),
			suffix=("add", "create", "new"),
			more_aliases=("addevent", "createevent", "newevent"),
		)
	)
	async def addevent(self, ctx, *args):
		"""
		Add events to the Google Calendar

		Usage:
		```
		++events.add <Title> on <Start Time>
		++events.add <Title> on <Start Time> to <End Time>
		++events.add <Title> on <Start Time> to <End Time> in <Class Name>
		```
		Examples:
		```
		++events.add Compilers HW 3 on April 10 at 11:59pm
		++events.add Calculus Moed Alef on February 9, 2021 at 8:30 am to 10:30 am
		++events.add Compilers HW 3 on April 10 at 11:59pm in Lev 2023
		```
		Arguments:
		**<Title>**: The name of the event to add.
		**<Start Time>**: The start time of the event.
		**<End Time>**: The end time of the event. If not specified, the start time is used.
		**<Class Name>**: The calendar to add the event to. Only necessary if you have more than one class role.
		"""
		message = " ".join(args)
		grad_year = None
		campus = None
		summary = None
		times = None
		# separate summary from rest of message
		if " on " in message:
			[summary, times] = message.split(" on ", 1)
		elif " at " in message:
			[summary, times] = message.split(" at ", 1)
		if not times:
			raise FriendlyError(
				"Expected 'on' or 'at' to separate title from time.",
				ctx.channel,
				ctx.author,
			)
		# check if calendar specified at the end
		if " in " in times:
			[times, calendar] = times.split(" in ", 1)
			try:
				grad_year, campus = self.finder.extract_year_and_campus(calendar)
				# check that specified calendar is one of the user's roles
				class_roles = self.finder.get_class_roles(ctx.author)
				if (grad_year, campus) not in class_roles:
					raise ClassRoleError(
						"You can not add events to the calendar of another class."
					)
			except (ClassRoleError, ClassParseError) as error:
				raise FriendlyError(error.args[0], ctx.channel, ctx.author)
		# separate start and end times
		if " to " in times:
			[start, end] = times.split(" to ", 1)
		else:
			start = times
			end = None
		if not grad_year or not campus:
			try:
				grad_year, campus = self.finder.get_class_info_from_role(ctx.author)
			except ClassRoleError as error:
				raise FriendlyError(error.args[0], ctx.channel, ctx.author)
		calendar_id = self.finder.get_calendar_id(grad_year, campus)
		event = self.calendar.add_event(calendar_id, summary, start, end)
		embed = self.calendar_embedder.embed_event("Event created successfully", event)
		await ctx.send(embed=embed)

	@commands.command(
		**build_aliases(
			name="calendar.grant",
			prefix=("calendar", "events"),
			suffix=("grant", "manage", "allow", "invite"),
		)
	)
	async def addmanager(self, ctx, email):
		"""
		Add a Google account as a manager of your class's calendar

		Usage:
		```
		++calendar.grant <email>
		```
		Arguments:
		> **<email>**: Email address to add as a calendar manager
		"""
		if not is_email(email):
			raise FriendlyError("Invalid email address", ctx.channel, ctx.author)
		class_roles = self.finder.get_class_roles(ctx.author)
		for grad_year, campus in class_roles:
			calendar_id = self.finder.get_calendar_id(grad_year, campus)
			# add manager to calendar
			self.calendar.add_manager(calendar_id, email)
			embed = self.calendar_embedder.embed_success(
				f"Successfully added manager to {campus} {grad_year} calendar."
			)
			await ctx.send(embed=embed)

	@commands.command(name="createcalendar")
	@commands.has_permissions(manage_roles=True)
	async def createcalendar(self, ctx, *args):
		"""
		Create a public calendar on the service account

		Usage:
		```
		++createcalendar JCT CompSci Lev 2020
		```
		Arguments:
		> **JCT CompSci Lev 2020**: name of the calendar to create
		"""
		summary = " ".join(args)
		# create calendar
		new_calendar = self.calendar.create_calendar(summary)
		embed = self.calendar_embedder.embed_success(
			f"Successfully created '{new_calendar['summary']}' calendar.",
			f"Calendar ID: {new_calendar['id']}",
		)
		await ctx.send(embed=embed)

	@commands.command(name="listcalendars")
	@commands.has_permissions(manage_roles=True)
	async def listcalendars(self, ctx):
		"""
		Get a list of all calendars on the service account

		Usage:
		```
		++listcalendars
		```
		"""
		# get calendar list
		calendars = self.calendar.get_calendar_list()
		details = (f"{calendar['summary']}: {calendar['id']}" for calendar in calendars)
		await ctx.send("\n".join(details))


# setup functions for bot
def setup(bot):
	bot.add_cog(CalendarCog(bot))