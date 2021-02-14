import discord

from utils.enums.PollType import PollType

class DiscordRepository:
    def __init__(self, bot):
        self.bot = bot

    def fetch_channels_from_guild(self, guildId):
        return self.bot.get_guild(guildId).text_channels

    async def fetch_list_messages(self, guildId, pollType):
        channels = self.fetch_channels_from_guild(guildId)
        for channel in channels:
            if(channel.name == pollType):
                messages = await channel.history(limit=1000).flatten()
                return messages


                