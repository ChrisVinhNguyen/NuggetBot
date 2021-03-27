import discord
import random

from utils.enums.PollType import PollType
from utils.models.Poll import PollEntry
from utils.api.DiscordRepository import DiscordRepository


class DemocracyManager:
    def __init__(self, bot):
        self.discordUtils = DiscordRepository(bot)

    def clamp(self, n, minn, maxn):
        if n < minn:
            return minn
        elif n > maxn:
            return maxn
        else:
            return n

    async def get_poll_data(self, guildId, pollType, numberOfResults=None):
        messages = await self.discordUtils.fetch_list_messages(guildId, pollType)
        pollData = []

        if numberOfResults is not None:
            if numberOfResults > len(messages):
                pollData.append(discord.Embed(
                    title="Oops!", description="Requested number of results exceed number of entries in the " + pollType, color=0xFF0000))
            elif numberOfResults < 1:
                pollData.append(discord.Embed(
                    title="Oops!", description="Requested number of results must be at least 1", color=0xFF0000))

            numberOfResults = self.clamp(numberOfResults, 1, len(messages))
            messages = random.sample(messages, numberOfResults)

        if pollType is PollType.watch:
            for message in messages:
                miniEmbed = self.map_embed_to_mini(message.embeds[0])
                pollData.append(miniEmbed)
        elif pollType is PollType.activity or PollType.activity_secondary:
            for message in messages:
                pollData.append(discord.Embed(title=message.content, color=0xFF953B).set_footer(
                    text="Press 👍 if you want to do this and 👎 if you don't"))


        return pollData

    def map_embed_to_mini(self, embed):
        embedDict = embed.to_dict()
        print(embedDict)
        miniEmbed = discord.Embed(
            title=embedDict["title"], url=embedDict["url"], color=0xFF953B)

        miniEmbed.add_field(name="Release Date", value=self.get_field_value(
            embedDict, "Release Date"), inline=True)
        miniEmbed.add_field(name="Runtime", value=self.get_field_value(
            embedDict, "Runtime"), inline=True)
        miniEmbed.add_field(name="Rating", value=self.get_field_value(
            embedDict, "Rating"), inline=True)
        miniEmbed.add_field(name="Submitter", value=self.get_field_value(
            embedDict, "Submitter"), inline=True)
        miniEmbed.set_thumbnail(url=embedDict["image"]["url"])
        miniEmbed.set_footer(
            text="Press 👍 if you want to watch this and 👎 if you don't")

        return miniEmbed

    def get_field_value(self, data, title):
        fields = data["fields"]
        for field in fields:
            if field["name"] == title:
                return field["value"]
        return "No " + title + " available"

    def filter_users(self, users):
        for user in users:
            if user.bot:
                users.remove(user)
        return users

    def get_users_names(self, users):
        if len(users) == 0:
            return "None"

        names = ""
        for user in users:
            names += user.display_name
            if(user != users[-1]):
                names += ", "
        return names

    def get_score(self, entry):
        score = len(entry.votesFor) - len(entry.votesAgainst)
        print(entry.message.embeds[0].title + " "+ str(score))
        return score

    def create_poll_results(self, entries):
        embed = discord.Embed(title="Results", color=0x2D7EFF)
        
        for entry in entries:
            self.filter_users(entry.votesFor)
            self.filter_users(entry.votesAgainst)

        sortedEntries = sorted(entries, key=self.get_score, reverse=True)
        for entry in sortedEntries:
            if(len(entry.votesFor) > 0 or len(entry.votesAgainst) > 0):
                embed.add_field(name=entry.message.embeds[0].title, value="Score: " + str(self.get_score(entry)), inline=True)
                embed.add_field(name="👍", value=self.get_users_names(
                    entry.votesFor), inline=True)
                embed.add_field(name="👎", value=self.get_users_names(
                    entry.votesAgainst), inline=True)

        if len(embed.fields) == 0:
            embed.description = "No votes yet"

        return embed

    async def close_poll(self, poll):
        for entry in poll.entries:
            await entry.message.clear_reactions()
        resultEmbed = poll.result.embeds[0]
        resultEmbed.set_footer(text="Poll is closed")
        await poll.result.edit(embed=resultEmbed.set_footer(text="Poll is closed"))
