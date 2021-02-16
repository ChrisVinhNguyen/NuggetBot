import discord

from discord.ext import commands
from utils.DemocracyManager import DemocracyManager
from utils.enums.PollType import PollType
from utils.enums.ChannelNames import ChannelNames
from utils.api.DiscordRepository import DiscordRepository

class Democracy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.democracyManager = DemocracyManager(bot)
        self.discordRepository = DiscordRepository(bot)
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Democracy is loaded")

    # Commands
    @commands.command(name = 'pollWatch', help = 'Start a what to watch poll in the democracy channel')
    async def watch_poll(self, ctx):
        print('Starting watch poll')
        pollData = await self.democracyManager.get_poll_data(ctx.guild.id, PollType.watch)
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.democracy)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + PollType.watch))
        else: 
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Poll's up!", description = "Check democracy for the poll"))

            await channel.send(embed = discord.Embed(title="Vote!", description = "React to the movie you want/don't want to watch"))
            for data in pollData:
                message = await channel.send(embed = data)
                await message.add_reaction('👍')
                await message.add_reaction('👎')


    @commands.command(name = 'pollActivity', help = 'Start a what to do poll in the democracy channel')
    async def activity_poll(self, ctx):
        print('Starting activity poll')
        pollData = await self.democracyManager.get_poll_data(ctx.guild.id, PollType.activity)
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.democracy)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + PollType.activity))
        else: 
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Poll's up!", description = "Check democracy for the poll"))

            await channel.send(embed = discord.Embed(title="Vote!", description = "React to what you want/don't want to do"))
            for data in pollData:
                message = await channel.send(embed = data)
                await message.add_reaction('👍')
                await message.add_reaction('👎')

def setup(client):
    client.add_cog(Democracy(client))