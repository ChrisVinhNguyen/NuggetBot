import discord

from utils.api.DiscordUtils import DiscordUtils

class MessageParser:
    def __init__(self, bot):
        self.discordUtils = DiscordUtils(bot)

    async def get_poll_embed(self, guildId, pollType):
        messages = await self.discordUtils.fetch_list_messages(guildId, pollType)
        if(len(messages) == 0):
            return discord.Embed(title="Oops!", description = "There is nothing in " + pollType)
        
        poll = ""
        for message in messages:
            poll += message.content
            poll += "\n"

        return discord.Embed(title="Vote!", description=poll)

    