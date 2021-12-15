# Classe permettant de définir un album

import datetime

class Album:
    rank: int
    trend: str
    title: str
    artist: str
    editor: str
    last_week_rank: int
    week_in: int
    best_rank: int
    certification: str = None
    certification_date: datetime.date = None

    def __init__(self, rank, trend, title, artist, editor, last_week_rank, week_in, best_rank, certification=None, certification_date=None):
        self.rank = rank
        self.trend = trend
        self.title = title
        self.artist = artist
        self.editor = editor
        self.last_week_rank = last_week_rank
        self.week_in = week_in
        self.best_rank = best_rank
        self.certification = certification
        self.certification_date = certification_date
