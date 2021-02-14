from dataclasses import dataclass

@dataclass
class Movie:
    title: str = "No title available"
    url: str = ""
    plotOutline: str = "No summary available"
    runtime: str = "No runtime available"
    rating: str = "No rating available"
    releaseDate: str = "No release date available"
    submitter: str = ""
    coverUrl: str = ""
