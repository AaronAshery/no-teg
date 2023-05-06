from no_teg import Game


class FIFA(Game):
    """
    A subclass of Game to represent FIFA.
    """

    def __init__(self):
        self.name = "FIFA"
        self.rec_players = 8  # useless?
        self.rec_tourney = "Single_Elimination"
        self.labels = []
