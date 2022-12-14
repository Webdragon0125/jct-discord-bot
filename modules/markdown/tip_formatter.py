from nextcord.ext import commands

from .formatting_tip import Tip

formats = {
    "italics": Tip("ππ΅π’π­πͺπ€π΄", "*italics*", "\\*italics* or \\_italics_"),
    "bold": Tip("ππΌπΉπ±", "**bold text**", "\\**bold text**"),
    "underline": Tip("UΝnΝdΝeΝrΝlΝiΝnΝeΝ", "__underline__", "\\__underline__"),
    "strikethrough": Tip("SΜΆtΜΆrΜΆiΜΆkΜΆeΜΆtΜΆhΜΆrΜΆoΜΆuΜΆgΜΆhΜΆ", "~~strikethrough~~", "\\~~strikethrough~~"),
    "spoiler": Tip("βββββββ (Spoiler)", "||spoiler|| (click to reveal)", "\\||spoiler||"),
    "inline": Tip("πΈπππππ ππππ", "`inline code`", "\\`inline code`"),
    "codeblock": Tip(
        "π±ππππ ππππ",
        '```cpp\ncout << "This is a code block" << endl;\n```',
        "\\```cpp\n// replace this with your code\n```",
        footer=(
            "Copy the snippet above into a message and insert your code in the"
            " middle. You can also change the syntax highlighting language by"
            " replacing `cpp` with another language, for example, `js`, `py`,"
            " or `java`."
        ),
    ),
}


def all_markdown_tips() -> str:
    """return a list of all markdown tips"""
    message = "**__Markdown Tips__**\n\n"
    for format in formats:
        message += formats[format].short_message() + "\n\n"
    return message


def individual_info(format: str) -> str:
    """return info for given format"""
    return formats[format].long_message()
