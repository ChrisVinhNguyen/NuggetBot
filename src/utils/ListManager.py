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
            movieData = self.get_movie_data(movie)
            return self.map_movie_to_embed(movieData, True, submitter), movieData


    def get_movie_data(self, movie):
        movieName = ' '.join(movie)
        return self.imdbRepository.search_movie(movieName)
        

    def map_movie_to_embed(self, movies, isConfirmation, submitter):
        if(len(movies) == 0):
            return discord.Embed(title="Oops!", description = "Nothing was found!")
        movie = self.imdbRepository.fetch_movie_details(movies[0])
        movie.submitter = submitter

        print(movie)
    
        embed = discord.Embed(title= movie.title, url = movie.url, description = movie.plotOutline, color=0x109319)
        embed.add_field(name = "Release Date", value = movie.releaseDate, inline = True)
        embed.add_field(name = "Runtime", value = movie.runtime, inline = True) 
        embed.add_field(name = "Rating", value = movie.rating, inline = True) 
        embed.add_field(name = "Submitter", value = movie.submitter, inline = False) 
        embed.set_image(url = movie.coverUrl)

        if (isConfirmation):
            embed.set_footer(text="Is this the movie you want to add? Press 👍 if yes and 👎 if not")
    
        return embed
