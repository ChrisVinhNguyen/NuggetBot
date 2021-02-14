from imdb import IMDb
from utils.models.Movie import Movie

class ImdbRepository:
    def __init__(self):
        self.imdb = IMDb()

    def search_movie(self, movieName):
        return self.imdb.search_movie(movieName)
    
    def fetch_movie_details(self, movie):
        self.imdb.update(movie, ["main"])

        movieData = Movie(url = self.imdb.get_imdbURL(movie))

        if "title" in movie:
            movieData.title = movie["title"]

        if "plot outline" in movie:
            movieData.plotOutline = movie["plot outline"]

        if "runtime" in movie:
            movieData.runtime = str(movie["runtimes"])
        
        if "rating" in movie:
            movieData.rating = str(movie["rating"])

        if "original air date" in movie:
            movieData.releaseDate = movie["original air date"]
        elif "year" in movie:
            movieData.releaseDate = movie["year"]

        if "cover url" in movie:
            movieData.coverUrl = movie["cover url"]
        
        return movieData
