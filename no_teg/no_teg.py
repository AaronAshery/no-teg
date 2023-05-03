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
    game : Game
        the game the tournament is managing
    players : list of Player/Team
        the players or teams that the tournament is managing
    matchups : dict of {int : dict}
        the matchups and associated data

    Methods
    -------
    add_player(player):
        adds a player or team to the tournament
    add_players(players):
        sets the players or teams of the tournament
    randomize_matchups():
        randomizes the order of the players
    start():
        starts the tournament by initializing all the matchups
    input_result():
        inputs the result of concluded matchup
    get_matchups():
        returns the tournament matchups
    print_matchups():
        prints the tournament matchups
    print_results():
        prints just the concluded tournament matchups
    """

    def __init__(self, game):
        """
        Constructs the attributes of the Tourney class.

        Players and matchups are empty upon construction.

        Parameters
        ----------
        game : Game
            the game the tournament is managing
        """

        self.game = game
        self.players = []
        self.matchups = {}

    def add_player(self, player: Player / Team):
        """
        Adds a player or team to the tournament.

        Parameters
        ----------
        player : Player / Team
            the player or team to be added

        Returns
        -------
        None
        """

        self.players.append(player)

    def add_players(self, players: list[Player / Team]):
        """
        Sets the players or teams of the tournament.

        Parameters
        ----------
        players : list of Player / Team
            the players or teams to be set in the tournament

        Returns
        -------
        None
        """

        self.players = players

    def randomize_matchups(self):
        """
        Randomizes the order of the players.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        np.random.shuffle(self.players)

    def start(self):
        """
        Starts the tournament by initializing all the matchups.

        Function specifics differ per tournament subclass.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass  # pragma: no cover

    def input_result(self):
        """
        Inputs the result of concluded matchup.

        Function specifics differ per tournament subclass.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        pass  # pragma: no cover

    def get_matchups(self):
        """
        Returns the tournaments matchups.

        Parameters
        ----------
        None

        Returns
        -------
        self.matchups : dict of {int : dict}
        """
        return self.matchups

    # can take in a round to print the round
    def print_matchups(self):
        """
        Prints the tournament matchups.

        Function specifics differ per tournament subclass.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        pass  # pragma: no cover

    def print_results(self):
        """
        Prints just the concluded tournament matchups.

        Function specifics differ per tournament subclass.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass  # pragma: no cover


class Single_Elimination(Tourney):
    """
    A subclass of Tourney to represent a single elimination tournament.

    Currently only supports tournaments with the amount of players being a power of 2.
    """

    def start(self):
        labels = self.game.get_labels()
        self.started = True
        num_rounds = np.ceil(np.log2(len(self.players)))
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
                for stat in labels:
                    self.matchups[matchup_counter][stat] = None
                matchup_counter += 1
                p1 += 2
                p2 += 2
            round_matches = round_matches // 2
            round += 1

    def input_result(self, matchup_id, away_score, home_score, stats):
        """
        Inputs the result of concluded matchup.

        Parameters
        ----------
        matchup_id : int
            the id corresponding to the matchup in which the score is being inputted
        away_score : int
            the score of the away team
        home_score : int
            the score of the home team
        extra_stats : list, optional
            the extra stats for the game the tournament is managing

        Returns
        -------
        None
        """

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
        if len(stats) == len(extra_labels):
            for i in range(len(stats)):
                self.matchups[matchup_id][extra_labels[i]] = stats[i]

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
    """
    A subclass of Tourney to represent a round robin tournament.

    Supports any number of players and each player plays eachother once.
    """

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

    def input_result(self, matchup_id, away_score, home_score, extra_stats=[]):
        self.matchups[matchup_id]["Home_Score"] = home_score
        self.matchups[matchup_id]["Away_Score"] = away_score
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


class Player:
    """
    A class to represent a player.

    ...

    Attributes
    ----------
    name : str
        the name of the player
    age : int
        the age of the player

    Methods
    -------
    set_age(age):
        sets the age of the player
    get_name():
        returns the name of the player
    """

    def __init__(self, name):
        """
        Constructs the attributes of the Player class.
        """

        self.name = name
        self.age = None

    def set_age(self, age):
        """
        Sets the age of the player.

        Parameters
        ----------
        age : int
            the age of the player

        Returns
        -------
        None
        """

        self.age = age

    def get_name(self):
        """ "
        Returns the name of the player.

        Parameters
        ----------
        None

        Returns
        -------
        self.name : str
        """
        return self.name


class Team:
    """
    A class to represent a Team of Players.

    ...

    Attributes
    ----------
    name : str
        the name of the team
    players : list of Player
        the players on the team

    Methods
    -------
    add_player(player):
        adds a player to the team
    add_players(players):
        sets the players of the team
    get_name():
        returns the name of the team
    get_players():
        returns the players of the team
    """

    def __init__(self, name: str):
        """
        Constructs the attributes of the Team class.
        """

        self.name = name
        self.players = []

    def add_player(self, player: Player):
        """
        Adds a player to the team.

        Parameters
        ----------
        player : Player
            the player to be added

        Returns
        -------
        None
        """

        self.players.append(player)

    def add_players(self, players: list[Player]):
        """
        Set the players of the team.

        Parameters
        ----------
        players : list of Player
            the players to be set on the team

        Returns
        -------
        None
        """

        self.players = players

    def get_name(self):
        return self.name

    def get_players(self):
        return self.players


def example1():  # pragma: no cover
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
