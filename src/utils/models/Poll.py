import discord

from dataclasses import dataclass

@dataclass
class Poll:
    messageIds: list = []
    resultId: str = ""

