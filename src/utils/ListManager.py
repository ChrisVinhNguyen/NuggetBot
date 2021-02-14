import discord

from utils.api.DiscordRepository import DiscordRepository
from utils.api.ImdbRepository import ImdbRepository

class ListManager:
    def __init__(self, bot):
        self.discordUtils = DiscordRepository(bot)
        self.imdbRepository = ImdbRepository()

    def get_activity_string(self, activity):
        return ' '.join(activity)

    def get_movie_embed(self, movie, submitter):
        if(len(movie) == 0):
            return discord.Embed(title="Oops!", description = "Nothing was passed in")
        else:
            movieData = self.get_movie_data(' '.join(movie))
            return self.map_movie_to_embed(movieData, True, submitter)


    def get_movie_data(self, movie):
        movieName = ' '.join(movie)
        return self.imdbRepository.search_movie(movieName)
        

    def map_movie_to_embed(self, movies, isConfirmation, submitter):
        if(len(movies) == 0):
            return discord.Embed(title="Oops!", description = "Nothing was found!")
        print(movies)
        movie = self.imdbRepository.fetch_movie_details(movies[0])
        movie.submitter = submitter
        print(movie)
        

        embed = discord.Embed(title= movie.title, url = movie.url, color=0x109319)
    
        return embed
