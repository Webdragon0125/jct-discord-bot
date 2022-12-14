from typing import Optional, Set

import nextcord
from nextcord.ext import commands

from database.person import Person
from utils.utils import one

from ..error.friendly_error import FriendlyError
from .weighted_set import WeightedSet

__search_weights = {
    "word": 2,
    "channel": 1,
    "email": 5,
}


async def search(
    name: Optional[str] = None,
    channel: Optional[nextcord.TextChannel] = None,
    email: Optional[str] = None,
) -> Set[Person]:
    """returns a list of people who best match the name and channel"""
    weights = WeightedSet()

    # add the people belonging to the category of the given channel (if any)
    if channel:
        for person in await Person.search_by_channel(channel.id):
            weights[person] += __search_weights["channel"]

    # search their name
    if name:
        for word in name.split():
            for person, similarity in await Person.search_by_name(word):
                weights[person] += __search_weights["word"] * similarity

    # add the people who have the email mentioned
    if email:
        for person in await Person.search_by_email(email):
            weights[person] += __search_weights["email"]

    return weights.heaviest_items()


async def search_one(
    sender: nextcord.Interaction[commands.Bot],
    name: Optional[str] = None,
    channel: Optional[nextcord.TextChannel] = None,
    email: Optional[str] = None,
) -> Person:
    """
    Returns a single person who best match the query, or raise a FriendlyError if it couldn't find exactly one.

    :param sender: An object with the send method where friendly errors will be sent to.
    :type sender: nextcord.Interaction
    :param name: The name of the person you want to search for (first, last, or both).
    :type name: Optional[str]
    :param channel: A channel the person is linked to.
    :type channel: Optional[nextcord.TextChannel]
    :param email: The email of the person you want to search for.
    :type email: Optional[str]
    """
    people = await search(name, channel, email)
    if not people:
        raise FriendlyError(
            f"Unable to find someone who matches your query. Check your spelling or"
            f" try a different query. If you still can't find them, You can add"
            f" them with `/email person add`.",
            sender,
        )
    if len(people) > 1:
        raise FriendlyError(
            "I cannot accurately determine which of these people you're"
            " referring to. Please provide a more specific query.\n"
            + ", ".join(person.name for person in people),
            sender,
        )
    return one(people)
