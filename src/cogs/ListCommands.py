import discord

from discord.ext import commands
from utils.ListManager import ListManager
from utils.enums.ChannelNames import ChannelNames
from utils.api.DiscordRepository import DiscordRepository

class Lists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listManager = ListManager(bot)
        self.discordRepository = DiscordRepository(bot)
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("List commands are loaded")

    # Commands
    @commands.command(name = 'addToWatch', help = 'Add a new movie/tv show to the watch list')
    async def add_to_watch(self, ctx, *args):
        print('Adding to watch list')
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.watch)
        await ctx.send(embed = self.listManager.get_movie_embed(args, ctx.author.display_name))


    @commands.command(name = 'addToActivity', help = 'Add a new activity to the activity list')
    async def add_to_activity(self, ctx, *args):
        print('Adding to activity list')
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.activity)
        if(len(args) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "Nothing was passed in"))
        else:
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Added!", description = "Entry added to the activity list"))
            message = await channel.send(self.listManager.get_activity_string(args))

def setup(client):
    client.add_cog(Lists(client))