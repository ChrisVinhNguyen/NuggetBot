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
        embed, movieData= self.listManager.get_movie_embed(args, ctx.author.display_name)
        message = await ctx.send(embed = embed)
        for embed in message.embeds:
            if embed.title != "Oops!":
                await message.add_reaction('👍')
                await message.add_reaction('👎')

        def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')

        reaction, user = await self.bot.wait_for('reaction_add', check = check)
        if (reaction.emoji == '👍'):
            await ctx.send(embed = discord.Embed(title="Added!", description = "Entry added to the watch list"))
            await channel.send(embed = self.listManager.map_movie_to_embed(movieData, False, ctx.author.display_name))
        else:
            await ctx.send(embed = discord.Embed(title="Sorry!", description = "Entry not added to the watch list. Try specifying the exact movie title"))
        await message.clear_reactions()
    


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