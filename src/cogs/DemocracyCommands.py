import discord

from discord.ext import commands
from utils.MessageManager import MessageManager
from utils.enums.PollType import PollType
from utils.enums.ChannelNames import ChannelNames
from utils.api.DiscordRepository import DiscordRepository

class Democracy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messageManager = MessageManager(bot)
        self.discordRepository = DiscordRepository(bot)
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Democracy is loaded")

    # Commands
    @commands.command(name = 'watch', help = 'Start a what to watch poll')
    async def watch_poll(self, ctx):
        print('Starting watch poll')
        pollData = await self.messageManager.get_poll_data(ctx.guild.id, PollType.watch)
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.democracy)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + PollType.watch))
        else: 
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Poll's up!", description = "Check democracy for the poll"))

            await channel.send(embed = discord.Embed(title="Vote!", description = "React to the movie you want to watch"))
            for data in pollData:
                message = await channel.send(data)
                await message.add_reaction('👍')


    @commands.command(name = 'activity', help = 'Start a what to do poll')
    async def activity_poll(self, ctx):
        print('Starting activity poll')
        pollData = await self.messageManager.get_poll_data(ctx.guild.id, PollType.activity)
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.democracy)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + PollType.activity))
        else: 
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Poll's up!", description = "Check democracy for the poll"))

            await channel.send(embed = discord.Embed(title="Vote!", description = "React to what you want to do"))
            for data in pollData:
                message = await channel.send(data)
                await message.add_reaction('👍')

def setup(client):
    client.add_cog(Democracy(client))