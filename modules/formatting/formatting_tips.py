from utils.utils import blockquote
from modules.error.friendly_error import FriendlyError
from discord.ext import commands


class FormattingTips:
	def __init__(self):
		# maps format name to pair containing preview markdown and escaped markdown
		self.formats = {
			"italics": ("*italics*", "\*italics* or \_italics_"),
			"bold": ("**bold text**", "\**bold text**"),
			"underline": ("__underline__", "\__underline__"),
			"strikethrough": ("~~strikethrough~~", "\~~strikethrough~~"),
			"spoiler": ("||spoiler|| (click to reveal)", "\||spoiler||"),
			"inline": ("`inline code`", "\`inline code`"),
			"codeblock": (
				'```cpp\ncout << "Code Block";\n```',
				'\```cpp\n// replace this with your code\ncout << "Code Block";\n```',
			),
		}
		# alternative ways to request formats (spaces and case is already ignored)
		self.aliases = {
			"italic": "italics",
			"inlinecode": "inline",
			"spoilers": "spoiler",
			"underlines": "underline",
			"code": "codeblock",
			"codeblocks": "codeblock",
			"codesnippet": "codeblock",
			"snippet": "codeblock",
			"strike": "strikethrough",
		}

	def all_markdown_tips(self) -> str:
		"""return a list of all markdown tips"""
		message = "**__Markdown Tips__**\n\n"
		for format in self.formats:
			(preview, escaped) = self.formats[format]
			message += f"{preview}\n"
			message += f"{blockquote(escaped)}\n\n"
		return message

	def individual_info(self, ctx: commands.Context, format: str) -> str:
		"""return info for given format"""
		normalized = self.__normalize(ctx, format)
		if normalized == "codeblock":
			return self.__codeblock_info()
		else:
			(preview, escaped) = self.formats[normalized]
			return (
				f"Did you know you can format your message with {preview}?\n\n"
				f"{blockquote(escaped)}\n\n"
				"Copy the snippet into a message replacing the text with your own."
			)

	def __normalize(self, ctx: commands.Context, format: str) -> str:
		"""normalize format to match format keys"""
		# convert to lowercase
		lower_format = format.lower()
		# check if inputted format is recognized
		if lower_format in self.formats:
			return lower_format
		# check for aliases
		elif lower_format in self.aliases:
			return self.aliases[lower_format]
		# format is not recognized
		else:
			raise FriendlyError(
				f"'{format}' is not a recognized format.", ctx.channel, ctx.author
			)

	def __codeblock_info(self) -> str:
		"""Returns info about using codeblocks."""
		(_, escaped) = self.formats["codeblock"]
		return (
			"Did you know you can format your code with a monospace font and syntax"
			f" highlighting on Discord?\n\n{blockquote(escaped)}\n\nCopy the snippet"
			" above into a message and insert your code in the middle. You can also"
			" change the syntax highlighting language by replacing `cpp` with another"
			" language, for example, `js`, `py`, or `java`."
		)
