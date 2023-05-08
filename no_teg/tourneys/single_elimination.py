from no_teg import Tourney
import numpy as np


class Single_Elimination(Tourney):
    """
    A subclass of Tourney to represent a single elimination tournament.

    Currently only supports tournaments with the amount of players being a power of 2.
    """

    def start(self):
        labels = self.game.get_labels()
        self.started = True
        num_rounds = np.ceil(np.log2(len(self.players)))
        num_players = len(self.players)
        num_byes = int(2**num_rounds - num_players)

        matchup_counter = 1
        p = 0
        round_matches = (len(self.players) + num_byes) // 2  # players power of 2
        round = 1
        updating_round_matches = 0
        while round_matches > 0:
            updating_round_matches += round_matches
            for i in range(round_matches):
                if round == 1:
                    home = self.players[p].get_name()
                    p += 1

                    if i < round_matches - num_byes:
                        away = self.players[p].get_name()
                        p += 1
                    else:
                        away = "Bye"
                else:
                    home, away = None, None

                if round != num_rounds:
                    next = updating_round_matches + (i // 2) + 1
                else:
                    next = None

                self.matchups[matchup_counter] = {
                    "Away": away,
                    "Home": home,
                    "Next": next,
                    "Away_Score": None,
                    "Home_Score": None,
                }

                for stat in labels:
                    self.matchups[matchup_counter][stat] = None
                matchup_counter += 1
            round_matches = round_matches // 2
            round += 1

        for i in range(len(self.matchups)):
            away = self.matchups[i + 1]["Away"]
            if away == "Bye":
                self.input_result(i + 1, 0, 3, [])

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
            self.matchups[matchup_id]["Home_Score"] = None
            self.matchups[matchup_id]["Away_Score"] = None
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

    def print_matchups(self):  # pragma: no cover
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
