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
        embed = await self.messageParser.get_poll_embed(ctx.guild.id, PollType.watch)
        await ctx.send(embed = embed)


    @commands.command(name = 'activity', help = 'Start a what to do poll')
    async def activity_poll(self, ctx):
        print('Starting activity poll')
        embed = await self.messageParser.get_poll_embed(ctx.guild.id, PollType.activity)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Democracy(client))