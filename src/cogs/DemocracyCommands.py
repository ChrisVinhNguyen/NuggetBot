import discord

from discord_slash import cog_ext, SlashContext
from discord.ext import commands
from utils.DemocracyManager import DemocracyManager
from utils.enums.PollType import PollType
from utils.enums.ChannelNames import ChannelNames
from utils.models.Poll import Poll
from utils.models.Poll import PollEntry
from utils.api.DiscordRepository import DiscordRepository

MAX_ACTIVE_POLLS = 5

class Democracy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.democracyManager = DemocracyManager(bot)
        self.discordRepository = DiscordRepository(bot)
        self.pollList = []
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Democracy is loaded")

    # Commands
    @cog_ext.cog_subcommand(base = "Democracy", name = 'pollWatch', description = 'Start a what to watch poll in the democracy channel')
    async def watch_poll(self, ctx: SlashContext):
        print('Starting watch poll')
        await self.createPoll(ctx = ctx, pollType = PollType.watch)


    @cog_ext.cog_subcommand(base = "Democracy", name = 'pollWatchRandom', description = 'Start a what to watch poll in the democracy channel with random entries from the watch list')
    async def watch_poll_random(self, ctx, numberOfMovies: int):
        print('Starting watch poll')
        await self.createPoll(ctx = ctx, pollType = PollType.watch, numberOfResults = numberOfMovies)


    @cog_ext.cog_subcommand(base = "Democracy", name = 'pollActivity', description = 'Start a what to do poll in the democracy channel')
    async def activity_poll(self, ctx):
        print('Starting activity poll')
        await self.createPoll(ctx = ctx, pollType = PollType.activity)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if (not user.bot and (reaction.emoji == '👍' or reaction.emoji == '👎')):
            await self.updateResults(reaction = reaction)


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if (not user.bot and (reaction.emoji == '👍' or reaction.emoji == '👎')):
            await self.updateResults(reaction = reaction)
    

    async def updateResults(self, reaction):
        for poll in self.pollList:
            for entry in poll.entries:
                if (entry.message.id == reaction.message.id):
                    users = await reaction.users().flatten()
                    if (reaction.emoji == '👍'):
                        entry.votesFor = users
                    elif (reaction.emoji == '👎'):
                        entry.votesAgainst = users
                    await poll.result.edit(embed = self.democracyManager.create_poll_results(poll.entries))


    async def createPoll(self, ctx, pollType, numberOfResults = None):
        pollData = await self.democracyManager.get_poll_data(ctx.guild.id, pollType, numberOfResults)
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.democracy)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + pollType, color=0xFF0000))
        else: 
            entries = []
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Poll's up!", description = "Check democracy for the poll"))

            await channel.send(embed = discord.Embed(title="Vote!", description = "React to cast your vote", color = 0x2F329F))
            for data in pollData:
                message = await channel.send(embed = data)
                if data.title != "Oops!":
                    votesFor = []
                    votesAgainst = []
                    for reaction in message.reactions:
                        if (reaction.emoji == '👍'):
                            votesFor = await reaction.users().flatten()
                        elif (reaction.emoji == '👎'):
                            votesAgainst = await reaction.users().flatten()
                
                    entries.append(PollEntry(message, votesFor, votesAgainst))    
            result = await channel.send(embed = self.democracyManager.create_poll_results(entries))
            poll = Poll(entries, result)
            await self.addPollToQueue(poll)

            for entry in entries:
                if data.title != "Oops!":
                    await entry.message.add_reaction('👍')
                    await entry.message.add_reaction('👎')    

    
    async def addPollToQueue(self, poll):
        self.pollList.append(poll)
        if(len(self.pollList) > MAX_ACTIVE_POLLS):
            poll = self.pollList[0]
            await self.democracyManager.close_poll(poll)
            self.pollList.pop(0)


def setup(client):
    client.add_cog(Democracy(client))