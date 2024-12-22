class MovieData:
    """
    MovieData class to define Movie Objects from API
    """
    def __init__(self, id, title, overview, poster, vote_average, vote_count):
        self.id = id
        self.title = title
        self.overview = overview
        self.poster = 'https://image.tmdb.org/t/p/w500/' + poster if poster else None
        self.vote_average = vote_average
        self.vote_count = vote_count
