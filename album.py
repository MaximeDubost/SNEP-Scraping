# Classe permettant de définir un album

class Album:
    rank: int
    trend: str
    title: str
    artist: str
    editor: str
    last_week_rank: int
    week_in: int
    best_rank: int

    def __init__(self, rank, trend, title, artist, editor, last_week_rank, week_in, best_rank):
        self.rank = rank
        self.trend = trend
        self.title = title
        self.artist = artist
        self.editor = editor
        self.last_week_rank = last_week_rank
        self.week_in = week_in
        self.best_rank = best_rank
