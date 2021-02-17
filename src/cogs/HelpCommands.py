import discord

from discord_slash import cog_ext, SlashContext
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Help is loaded")

    # Commands
    @cog_ext.cog_subcommand(base = "Help", name = 'all', description = 'Show the entire help message')
    async def help_all(self, ctx: SlashContext):
        print('Sending help message')
        helpText = "Hi I'm NuggetBot, I can manage the watch/activity lists on this server and conduct polls for what to do/watch"
        print(helpText)
        embed = discord.Embed(title= "Help", url = "https://github.com/ChrisVinhNguyen/NuggetBot", description = helpText, color=0x109319)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Help(client))