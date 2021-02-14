import discord

from utils.api.DiscordRepository import DiscordRepository

class MessageManager:
    def __init__(self, bot):
        self.discordUtils = DiscordRepository(bot)

    async def get_poll_data(self, guildId, pollType):
        messages = await self.discordUtils.fetch_list_messages(guildId, pollType)
        messageStrings = []
        for message in messages:
            messageStrings.append(message.content)
        return messageStrings