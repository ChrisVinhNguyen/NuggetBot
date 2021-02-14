import discord

from utils.api.DiscordRepository import DiscordRepository
from utils.api.ImdbRepository import ImdbRepository

class ListManager:
    def __init__(self, bot):
        self.discordUtils = DiscordRepository(bot)
        self.imdbRepository = ImdbRepository()
