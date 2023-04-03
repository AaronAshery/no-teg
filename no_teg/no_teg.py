from __future__ import annotations
import numpy as np


class Game:
    """
    A class to represent a game.

    ...

    Attributes
    ----------
    name : str
        name of the game
    rec_players : int
        amount of players recommended
    rec_tourney : Tourney
        tournament type recommended

    Methods
    -------
    set_name(name):
        Sets the name of the game.
    set_rec_players(rec_players):
        Sets the recommended amount of players.
    set_rec_tourney(rec_tourney):
        Sets the recommended tournament type.
    set_labels(labels):
        Sets the labels for additional stat tracking for the game.
    get_labels():
        Gets the labels for the game.
    """

    def __init__(self):
        """
        Constructs the attributes of the Game class.

        Everything is empty upon construction and will need to be set with the class methods.

        Parameters
        ----------
        None
        """

        self.name = None
        self.rec_players = None
        self.rec_tourney = None
        self.labels = []

    def set_name(self, name: str):
        """
        Sets the name of the game.

        Parameters
        ----------
        name : str
            the name of the person

        Returns
        -------
        None
        """

        self.name = name

    def set_rec_players(self, rec_players: int):
        """
        Sets the recommended amount of players.

        Parameters
        ----------
        rec_players : int
            the recommended amount of players

        Returns
        -------
        None
        """
        self.rec_players = rec_players

    def set_rec_tourney(self, rec_tourney):
        """
        Sets the recommended tournament type.

        Parameters
        ----------
        rec_tourney : Tourney
            the recommended tournament type

        Returns
        -------
        None
        """
        self.rec_tourney = rec_tourney

    def set_labels(self, labels: list[str]):
        """
        Sets the labels for additional stat tracking for the game.

        Parameters
        ----------
        labels : list of str
            the labels for additional stat tracking

        Returns
        -------
        None
        """
        self.labels = labels

    def get_labels(self):
        """
        Gets the labels for the game.

        Parameters
        ----------
        None

        Returns
        -------
        self.labels : list of str
            the labels for additional stat tracking
        """
        return self.labels


class FIFA(Game):
    """
    A subclass of Game to represent FIFA.
    """

    def __init__(self):
        self.name = "FIFA"
        self.rec_players = 8  # useless?
        self.rec_tourney = "Single_Elimination"
        self.labels = []


class Tourney:
    """
    A interface-like class to represent a tournament.

    ...

    Attributes
    ----------
    game: Game
        the game the tournament is managing
    players: list of Player/Team
        the players or teams that the tournament is managing
    matchups: dict of {int : dict}
        the matchups and associated data

    Methods
    -------
    add_player(player):
        adds a player to the tournament
    add_players(players):
        sets the players of the tournament
    randomize_matchups():
        randomizes the order of the players
    start():
        starts the tournament by initializing all the matchups
    input_result():
        inputs the result of concluded matchup
    get_matchups():
        returns the tournament matchups
    print_matchups():
        prints the tournament machups
    print_results():
        prints just the concluded tournament matchups
    """

    def __init__(self, game):
        self.game = game
        self.players = []
        self.matchups = {}

    def add_player(self, player: Player / Team):
        self.players.append(player)

    def add_players(self, players: list[Player / Team]):
        self.players = players

    def randomize_matchups(self):
        np.random.shuffle(self.players)

    def start(self):
        """Set all matchups"""
        pass  # pragma: no cover

    def input_result(self):
        pass  # pragma: no cover

    def get_matchups(self):
        return self.matchups

    # can take in a round to print the round
    def print_matchups(self):
        pass  # pragma: no cover

    def print_results(self):
        pass  # pragma: no cover


class Single_Elimination(Tourney):
    # ex matchups 4 person SE {
    #    1:{Home: "Aaron", Away: "Xandra", Next: 3, Home_Score: 2, Away_Score: 1},
    #    2:{Home: "Tiffany", Away: "Lucas", Next: 3, Home_Score: 4, Away_Score: 0},
    #    3:{Home: "Aaron", Away: "Lucas", Next: None, Home_Score: None, Away_Score: None}
    #   }
    def start(self):
        extra_labels = self.game.get_labels()
        # print("EXTRA LABELS: " + str(extra_labels))
        # set entire bracket
        # assume number of participants is a power of 2
        self.started = True
        # total_matches = len(self.players) - 1
        num_rounds = np.ceil(np.log2(len(self.players)))
        # num_byes = num_rounds**2 - len(self.players)
        matchup_counter = 1
        p1 = 0
        p2 = 1
        round_matches = len(self.players) // 2  # players power of 2
        round = 1
        updating_round_matches = 0
        while round_matches > 0:
            updating_round_matches += round_matches
            for i in range(round_matches):
                if round == 1:
                    home, away = self.players[p1].get_name(), self.players[p2].get_name()
                else:
                    home, away = None, None
                if round != num_rounds:
                    next = updating_round_matches + (i // 2) + 1
                else:
                    next = None
                self.matchups[matchup_counter] = {
                    "Home": home,
                    "Away": away,
                    "Next": next,
                    "Home_Score": None,
                    "Away_Score": None,
                }
                for stat in extra_labels:
                    self.matchups[matchup_counter][stat] = None
                matchup_counter += 1
                p1 += 2
                p2 += 2
            round_matches = round_matches // 2
            round += 1

    def input_result(self, matchup_id, away_score, home_score, extra_stats=[]):
        self.matchups[matchup_id]["Home_Score"] = home_score
        self.matchups[matchup_id]["Away_Score"] = away_score
        home = self.matchups[matchup_id]["Home"]
        away = self.matchups[matchup_id]["Away"]
        if home_score > away_score:
            winner = home
        elif away_score > home_score:
            winner = away
        else:
            winner = "Tie"
            print("This format does not support ties")  # dont let ties be input
            return False
        next = self.matchups[matchup_id]["Next"]
        if next is not None:
            if matchup_id % 2 == 0:
                self.matchups[next]["Home"] = winner
            else:
                self.matchups[next]["Away"] = winner
        extra_labels = self.game.get_labels()
        if len(extra_stats) == len(extra_labels):
            for i in range(len(extra_stats)):
                self.matchups[matchup_id][extra_labels[i]] = extra_stats[i]

    def print_matchups(self):
        for i in range(len(self.matchups)):
            matchup_id = i + 1
            home = self.matchups[matchup_id]["Home"]
            away = self.matchups[matchup_id]["Away"]
            if home is not None and away is not None:
                print("{:d}: {:s} (A) vs {:s} (H)".format(matchup_id, away, home))

    def print_results(self):  # pragma: no cover
        for i in range(len(self.matchups)):
            matchup_id = i + 1
            home = self.matchups[matchup_id]["Home"]
            away = self.matchups[matchup_id]["Away"]
            home_score = self.matchups[matchup_id]["Home_Score"]
            away_score = self.matchups[matchup_id]["Away_Score"]
            if home is not None and away is not None and home_score is not None and away_score is not None:
                print("{:d}: {:s} ({:d}) vs {:s} ({:d})".format(matchup_id, away, away_score, home, home_score))


# circle algorithm
class Round_Robin(Tourney):
    def start(self):
        extra_labels = self.game.get_labels()
        self.started = True
        matchup_counter = 1

        if len(self.players) % 2 == 1:
            num_players = len(self.players) + 1
            players = self.players + [Player('dummy')]
        else:
            num_players = len(self.players)
            players = self.players
        num_rounds = num_players - 1
        num_matches_per_round = num_players // 2

        # rounds not currently used but could be in the future
        rounds = []
        for round_number in range(num_rounds):
            matches = []
            for match in range(num_matches_per_round):
                home = players[match].get_name()
                away = players[-(match + 1)].get_name()
                if home != 'dummy' and away != 'dummy':
                    self.matchups[matchup_counter] = {
                        "Home": home,
                        "Away": away,
                        "Home_Score": None,
                        "Away_Score": None,
                    }
                    for stat in extra_labels:
                        self.matchups[matchup_counter][stat] = None
                    matchup_counter += 1

            rounds.append(matches)
            players.insert(1, players.pop())

    def print_matchups(self):
        for i in range(len(self.matchups)):
            matchup_id = i + 1
            home = self.matchups[matchup_id]["Home"]
            away = self.matchups[matchup_id]["Away"]
            if home is not None and away is not None:
                print("{:d}: {:s} (A) vs {:s} (H)".format(matchup_id, away, home))

    def print_results(self):  # pragma: no cover
        for i in range(len(self.matchups)):
            matchup_id = i + 1
            home = self.matchups[matchup_id]["Home"]
            away = self.matchups[matchup_id]["Away"]
            home_score = self.matchups[matchup_id]["Home_Score"]
            away_score = self.matchups[matchup_id]["Away_Score"]
            if home is not None and away is not None and home_score is not None and away_score is not None:
                print("{:d}: {:s} ({:d}) vs {:s} ({:d})".format(matchup_id, away, away_score, home, home_score))

    def input_result(self, matchup_id, away_score, home_score, extra_stats=[]):
        self.matchups[matchup_id]["Home_Score"] = home_score
        self.matchups[matchup_id]["Away_Score"] = away_score
        extra_labels = self.game.get_labels()
        if len(extra_stats) == len(extra_labels):
            for i in range(len(extra_stats)):
                self.matchups[matchup_id][extra_labels[i]] = extra_stats[i]


class Player:
    def __init__(self, name):
        self.name = name
        self.age = None

    def set_age(self, age):  # DOB?
        self.age = age

    def get_name(self):
        return self.name


class Team:
    def __init__(self, name: str):
        self.name = name
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)

    def add_players(self, players: list[Player]):
        self.players = players

    def get_name(self):
        return self.name

    def get_players(self):
        return self.players


def example1():
    MyTourney = Single_Elimination(FIFA())
    p1 = Player("Aaron")
    p2 = Player("Xandra")
    p3 = Player("Lucas")
    p4 = Player("Tiffany")
    MyTourney.add_players([p1, p2, p3, p4])
    MyTourney.randomize_matchups()
    MyTourney.start()
    MyTourney.print_matchups()
    MyTourney.input_result(1, 2, 3)
    MyTourney.input_result(2, 10, 1)
    MyTourney.input_result(3, 4, 1)
    MyTourney.print_results()
