import discord
import os

from discord.ext import commands

# Change the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Defaults'
)

# Initialize commands
bot = commands.Bot(
    command_prefix = commands.when_mentioned_or('/'),
    help_command = help_command
)

# Load commands on startup
for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Default Events
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


# Run the bot
bot.run("ODEwMzc0MTI3NDUzODYzOTc2.YCituA.o2RyLGx5iqqMu5Yma6qlqzDeR_M")

