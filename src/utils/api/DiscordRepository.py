import discord

from utils.enums.PollType import PollType
from utils.enums.ChannelNames import ChannelNames


class DiscordRepository:
    def __init__(self, bot):
        self.bot = bot

    def fetch_all_channels(self, guildId):
        return self.bot.get_guild(guildId).text_channels


    def fetch_channel(self, guildId, channelName):
        channels = self.fetch_all_channels(guildId)
        for channel in channels:
            if (channel.name == channelName):
                return channel

    
    def fetch_channel_by_id(self, guildId, channelId):
        channels = self.fetch_all_channels(guildId)
        for channel in channels:
            if (channel.id == channelId):
                return channel


    async def fetch_list_messages(self, guildId, pollType):
        channels = self.fetch_all_channels(guildId)
        for channel in channels:
            if(channel.name == pollType):
                messages = await channel.history(limit=1000).flatten()
                return messages


                