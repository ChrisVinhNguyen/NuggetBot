import discord

from discord.ext import commands

class BotLists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("List commands are loaded")

    # Commands
    @commands.command(name = 'addWatch', help = 'Add a new movie/tv show to the watch list')
    async def add_watch(self, ctx):
        print('Adding to watch list')
        message = await ctx.send("test")


    @commands.command(name = 'addActivity', help = 'Add a new activity to the activity list')
    async def add_activity(self, ctx):
        print('Adding to activity list')
        message = await ctx.send("test")

def setup(client):
    client.add_cog(BotLists(client))