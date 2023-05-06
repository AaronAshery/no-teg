from no_teg import Tourney, Player


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
                if match == 0 and round_number == 0:
                    home = players[match].get_name()
                    away = players[-(match + 1)].get_name()
                elif round_number % 2 == 0:
                    home = players[match].get_name()
                    away = players[-(match + 1)].get_name()
                else:
                    away = players[match].get_name()
                    home = players[-(match + 1)].get_name()

                if match >= num_matches_per_round // 2 and round_number != 0:
                    home, away = away, home

                if home != 'dummy' and away != 'dummy':
                    self.matchups[matchup_counter] = {
                        "Away": away,
                        "Home": home,
                        "Away_Score": None,
                        "Home_Score": None,
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

    def print_matchups(self):  #pragma: no cover
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
