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

def setup(client):
    client.add_cog(Democracy(client))