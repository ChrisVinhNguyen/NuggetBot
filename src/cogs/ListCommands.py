import discord
import asyncio

from discord_slash import cog_ext, SlashContext
from discord.ext import commands
from utils.ListManager import ListManager
from utils.enums.ChannelNames import ChannelNames
from utils.api.DiscordRepository import DiscordRepository

class Lists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listManager = ListManager(bot)
        self.discordRepository = DiscordRepository(bot)
        self.TIMEOUT = 60
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("List commands are loaded")

    # Commands
    @cog_ext.cog_subcommand(base = "Lists", name = 'addToWatch', description = 'Add a new movie/tv show to the watch list')
    async def add_to_watch(self, ctx, *movie):
        print('Adding to watch list')
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.watch)
        index = 0
        endOfList = False
        startOfList = True
        while (not endOfList):
            embed, endOfList, startOfList, movieData= self.listManager.get_movie_embed(movie, ctx.author.display_name, index)
            message = await ctx.send(embed = embed)
            
            if message.embeds[0].title != "Oops!":
                await message.add_reaction('👍')
                await message.add_reaction('👎')
                if(not startOfList):
                    await message.add_reaction('⬅️')
                if(not endOfList):
                    await message.add_reaction('➡️')
            else:
                break

            def check(reaction, user): 
                return user == ctx.author and message.id == reaction.message.id and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎' or str(reaction.emoji) == '⬅️' or str(reaction.emoji) == '➡️')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = self.TIMEOUT , check = check)
            except asyncio.TimeoutError:
                await ctx.send(embed = discord.Embed(title="Timeout!", description = "Entry not added to the watch list. Make your selection " + str(self.TIMEOUT) + " seconds"))
                await message.clear_reactions()
                break
            else:
                if (reaction.emoji == '👍'):
                    await ctx.send(embed = discord.Embed(title="Added!", description = "Entry added to the watch list"))
                    embed, endOfList, startOfList = self.listManager.map_movie_to_embed(movieData, False, ctx.author.display_name, index)
                    await channel.send(embed = embed)
                    await message.clear_reactions()
                    break
                elif (reaction.emoji == '👎'):
                    await ctx.send(embed = discord.Embed(title="Sorry!", description = "Entry not added to the watch list. Try specifying the exact movie title"))
                    await message.clear_reactions()
                    break
                elif (reaction.emoji == '➡️'):
                    index += 1
                    await message.delete()
                elif (reaction.emoji == '⬅️'):
                    index -= 1
                    await message.delete()
            


    @cog_ext.cog_subcommand(base = "Lists", name = 'addToActivity', description = 'Add a new activity to the activity list')
    async def add_to_activity(self, ctx, *activity):
        print('Adding to activity list')
        channel = self.discordRepository.fetch_channel(ctx.guild.id, ChannelNames.activity)
        if(len(activity) == 0):
            await ctx.send(embed = discord.Embed(title="Oops!", description = "Nothing was passed in"))
        else:
            if(ctx.channel != channel):
                await ctx.send(embed = discord.Embed(title="Added!", description = "Entry added to the activity list"))
            message = await channel.send(self.listManager.get_activity_string(activity))

   

def setup(client):
    client.add_cog(Lists(client))