import discord

from utils.api.DiscordUtils import DiscordUtils

class MessageParser:
    def __init__(self, bot):
        self.discordUtils = DiscordUtils(bot)

    async def get_poll_data(self, guildId, pollType):
        messages = await self.discordUtils.fetch_list_messages(guildId, pollType)
        messageStrings = []
        for message in messages:
            messageStrings.append(message.content)
        return messageStrings

    