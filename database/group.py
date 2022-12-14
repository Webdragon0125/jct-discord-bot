from functools import cached_property
from typing import Collection

import nextcord

import config
from database import sql
from database.campus import Campus


class Group:
    def __init__(self, id: int, grad_year: int, campus: Campus, role_id: int, calendar: str):
        self.__id = id
        self.__grad_year = grad_year
        self.__campus = campus
        self.__role_id = role_id
        self.__calendar = calendar

    @property
    def id(self) -> int:
        """The ID of the group as stored in the database."""
        return self.__id

    @property
    def grad_year(self) -> int:
        """The year in which this group is to graduate."""
        return self.__grad_year

    @property
    def campus(self) -> Campus:
        """The campus this Group belongs to"""
        return self.__campus

    @cached_property
    def role(self) -> nextcord.Role:
        """The Role associated with this Group."""
        role = nextcord.utils.get(config.guild().roles, id=self.__role_id)
        assert role is not None
        return role

    @property
    def calendar(self) -> str:
        """The calendar id associated with this Group. (Looks like an email address)"""
        return self.__calendar

    @property
    def name(self) -> str:
        """The name of this Group. (eg Lev 2021)"""
        return f"{self.campus.name} {self.__grad_year}"

    @classmethod
    async def get_group(cls, group_id: int) -> "Group":
        """Fetch a group from the database given its ID."""
        record = await sql.select.one(
            "groups", ("id", "grad_year", "campus", "role", "calendar"), id=group_id
        )
        assert record is not None
        return cls(*record)

    @classmethod
    async def get_groups(cls) -> Collection["Group"]:
        """Fetch a list of groups from the database"""
        records = await sql.select.many(
            "groups_campuses_view",
            (
                "group_id",
                "grad_year",
                "campus_id",
                "campus_name",
                "campus_channel",
                "role",
                "calendar",
            ),
        )
        return [
            cls(
                r["group_id"],
                r["grad_year"],
                Campus(r["campus_id"], r["campus_name"], r["campus_channel"]),
                r["role"],
                r["calendar"],
            )
            for r in records
        ]

    def __eq__(self, other):
        """Compares them by ID"""
        if isinstance(other, self.__class__):
            return self.__id == other.__id
        return False

    def __hash__(self):
        return hash(self.__id)
