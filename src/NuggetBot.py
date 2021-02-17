import discord
import os

from discord.ext import commands
from discord_slash import SlashCommand


# Change the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Defaults'
)

# Initialize commands
bot = commands.Bot(
    command_prefix = commands.when_mentioned_or('/'),
    help_command = None
)

slash = SlashCommand(bot, override_type = True, sync_commands = True)

# Load commands on startup
for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@slash.slash(name="help", description = "Show the help message")
async def help(ctx):
    helpText = "Hi I'm NuggetBot, I can manage the watch/activity lists on this server and conduct polls for what to do/watch"
    print(helpText)
    embed = discord.Embed(title= "Help", url = "https://github.com/ChrisVinhNguyen/NuggetBot", description = helpText, color=0x109319)
    await ctx.send(embed = embed)


# Default Events
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send(error)


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

