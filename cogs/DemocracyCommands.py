import discord

from discord.ext import commands
from utils.MessageParser import MessageParser
from utils.enums.PollType import PollType

class Democracy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messageParser = MessageParser(bot)
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Democracy is loaded")

    # Commands
    @commands.command(name = 'watch', help = 'Start a what to watch poll')
    async def watch_poll(self, ctx):
        print('Starting watch poll')
        pollData = await self.messageParser.get_poll_data(ctx.guild.id, PollType.watch)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + PollType.watch))
        else: 
            await ctx.send(embed = discord.Embed(title="Vote!", description = "React to the movie you want to watch"))
            
        for data in pollData:
            message = await ctx.send(data)
            await message.add_reaction('👍')


    @commands.command(name = 'activity', help = 'Start a what to do poll')
    async def activity_poll(self, ctx):
        print('Starting activity poll')
        pollData = await self.messageParser.get_poll_data(ctx.guild.id, PollType.activity)

        if (len(pollData) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "There is nothing in " + PollType.activity))
        else: 
            await ctx.send(embed = discord.Embed(title="Vote!", description = "React to what you want to do"))

        for data in pollData:
            message = await ctx.send(data)
            await message.add_reaction('👍')

def setup(client):
    client.add_cog(Democracy(client))