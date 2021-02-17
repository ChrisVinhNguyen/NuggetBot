import discord

from discord_slash import cog_ext, SlashContext
from discord.ext import commands
from utils.DemocracyManager import DemocracyManager
from utils.enums.PollType import PollType
from utils.enums.ChannelNames import ChannelNames
from utils.api.DiscordRepository import DiscordRepository

MAX_ACTIVE_POLLS = 10

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


    async def createPoll(self, ctx, pollType, numberOfResults = None):
        pollData = await self.democracyManager.get_poll_data(ctx.guild.id, pollType, numberOfResults)
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.democracy)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + pollType))
        else: 
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Poll's up!", description = "Check democracy for the poll"))

            await channel.send(embed = discord.Embed(title="Vote!", description = "React to the movie you want/don't want to watch"))
            for data in pollData:
                message = await channel.send(embed = data)
                if data.title != "Oops!":
                    await message.add_reaction('👍')
                    await message.add_reaction('👎')


def setup(client):
    client.add_cog(Democracy(client))