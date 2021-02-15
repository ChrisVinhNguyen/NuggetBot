import discord
import asyncio

from discord.ext import commands
from utils.ListManager import ListManager
from utils.enums.ChannelNames import ChannelNames
from utils.api.DiscordRepository import DiscordRepository

class Lists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listManager = ListManager(bot)
        self.discordRepository = DiscordRepository(bot)
        self.TIMEOUT = 30
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("List commands are loaded")

    # Commands
    @commands.command(name = 'addToWatch', help = 'Add a new movie/tv show to the watch list')
    async def add_to_watch(self, ctx, *args):
        print('Adding to watch list')
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.watch)
        index = 0
        endOfList = False
        while (not endOfList):
            embed, endOfList, movieData= self.listManager.get_movie_embed(args, ctx.author.display_name, index)
            message = await ctx.send(embed = embed)
            
            if message.embeds[0].title != "Oops!":
                await message.add_reaction('👍')
                await message.add_reaction('👎')
                if(not endOfList):
                    await message.add_reaction('➡️')
            else:
                break

            def check(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎' or str(reaction.emoji) == '➡️')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = self.TIMEOUT , check = check)
            except asyncio.TimeoutError:
                await ctx.send(embed = discord.Embed(title="Timeout!", description = "Entry not added to the watch list. Make your selection " + str(self.TIMEOUT) + " seconds"))
                await message.clear_reactions()
                break
            else:
                if (reaction.emoji == '👍'):
                    await ctx.send(embed = discord.Embed(title="Added!", description = "Entry added to the watch list"))
                    embed, endOfList = self.listManager.map_movie_to_embed(movieData, False, ctx.author.display_name, index)
                    await channel.send(embed = embed)
                    await message.clear_reactions()
                    break
                elif (reaction.emoji == '👎'):
                    await ctx.send(embed = discord.Embed(title="Sorry!", description = "Entry not added to the watch list. Try specifying the exact movie title"))
                    await message.clear_reactions()
                    break
                elif (reaction.emoji == '➡️'):
                    index += 1
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