import discord

from discord.ext import commands

class Democracy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Democracy is loaded")

    # Commands
    @commands.command(name = 'watch', help = 'Start a what to watch poll')
    async def watchPoll(self, ctx):
        print('Starting watch poll')
        response = "Watch poll"
        await ctx.send(response)


    @commands.command(name = 'activity', help = 'Start a what to do poll')
    async def activityPoll(self, ctx):
        print('Starting activity poll')
        response = "Activity poll"
        await ctx.send(response)

def setup(client):
    client.add_cog(Democracy(client))