from __future__ import annotations
import numpy as np
import pandas as pd

# no-teg is quick and dirty, in the future could evolve to a full scale tournament API


# game could be reduced to a pd df
# each game just a new row with their specs


# game interface
class Game:
    """Initialize new game"""

    def __init__(self):
        self.name = None
        self.rec_players = None
        self.rec_tourney = None
        self.labels = []

    def set_name(self, name: str):
        self.name = name

    def set_rec_players(self, rec_players: int):
        self.rec_players = rec_players

    def set_rec_tourney(self, rec_tourney):
        self.rec_tourney = rec_tourney

    def set_labels(self, labels: list[str]):
        self.labels = labels

    def get_labels(self):
        return self.labels


class FIFA(Game):
    def __init__(self):
        self.name = "FIFA"
        self.rec_players = 8  # useless?
        self.rec_tourney = "Single_Elimination"
        self.labels = []


# interface
class Tourney:
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

    def start(self, additional_stats=None):
        """Set all matchups"""
        pass

    def input_result(self):
        pass

    def get_matchups(self):
        return self.matchups

    # can take in a round to print the round
    def print_matchups(self):
        pass

    def print_results(self):
        pass


class Single_Elimination(Tourney):
    # ex matchups 4 person SE {
    #    1:{Home: "Aaron", Away: "Xandra", Next: 3, Home_Score: 2, Away_Score: 1},
    #    2:{Home: "Tiffany", Away: "Lucas", Next: 3, Home_Score: 4, Away_Score: 0},
    #    3:{Home: "Aaron", Away: "Lucas", Next: None, Home_Score: None, Away_Score: None}
    #   }
    def start(self):
        extra_labels = self.game.get_labels()
        print("EXTRA LABELS: " + str(extra_labels))
        # set entire bracket
        # assume number of participants is a power of 2
        self.started = True
        total_matches = len(self.players) - 1
        num_rounds = np.ceil(np.log2(len(self.players)))
        num_byes = num_rounds**2 - len(self.players)
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
            print("This format does not support ties")  # dont let teis be input
            return False
        next = self.matchups[matchup_id]["Next"]
        if next != None:
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
            if home != None and away != None:
                print("{:d}: {:s} (A) vs {:s} (H)".format(matchup_id, away, home))

    def print_results(self):
        for i in range(len(self.matchups)):
            matchup_id = i + 1
            home = self.matchups[matchup_id]["Home"]
            away = self.matchups[matchup_id]["Away"]
            home_score = self.matchups[matchup_id]["Home_Score"]
            away_score = self.matchups[matchup_id]["Away_Score"]
            if home != None and away != None and home_score != None and away_score != None:
                print("{:d}: {:s} ({:d}) vs {:s} ({:d})".format(matchup_id, away, away_score, home, home_score))


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
