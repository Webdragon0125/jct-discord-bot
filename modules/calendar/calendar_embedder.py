import re
from .event import Event
from typing import Iterable, Dict
import discord


class CalendarEmbedder:
	def __init__(self):
		self.timezone = "Asia/Jerusalem"

	def embed_event_list(
		self,
		title: str,
		events: Iterable[Event],
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
		self, title: str, event: Event, colour: discord.Colour = discord.Colour.green(),
	) -> discord.Embed:
		"""Embed an event with the summary, link, and dates"""
		embed = discord.Embed(title=title, colour=colour)
		# add overview of event to the embed
		embed.description = self.__get_formatted_event_details(event)
		embed.set_footer(text=self.__get_footer_text())
		return embed

	def __trim_text_links_preserved(self, text: str, max: int = 30) -> str:
		"""Trims a string of text to a maximum number of characters,
		but preserves links using markdown if they get cut off"""
		# trims the text normally
		trimmed = text[:max].strip() + "..." if len(text) > max else text
		# get the part before and after the text is cut off
		before_match = re.search(r"\S+$", text[:max])
		after_match = re.search(r"^\S+", text[max:])
		if before_match and after_match:
			# get the full word at the cut-off
			before = before_match.group(0)
			after = after_match.group(0)
			full = before + after
			# check if the word that got cut off is a link
			if re.match(r"^https?:\S*$", full):
				# replace link fragment with markdown link
				start = before_match.start()
				trimmed = text[:start] + f'[{before}...]({full} "{full}")'
		return trimmed

	def __get_formatted_event_details(self, event: Event) -> str:
		"""Format event as a markdown linked summary and the dates below"""
		info = f"**[{event.title()}]({event.link()})**\n"
		info += f"{event.date_range_str()}\n"
		if event.description():
			# trim to max 35 chars
			info += f"{self.__trim_text_links_preserved(event.description(), max=35)}\n"
		if event.location():
			# trim to max 30 chars
			info += f":round_pushpin: {self.__trim_text_links_preserved(event.location())}\n"
		return info

	def __get_footer_text(self):
		"""Return text about timezone to display at end of embeds with dates"""
		return f"Times are shown for {self.timezone}"