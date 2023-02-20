import numpy as np
import pandas as pd
# from enum import Enum


class Master:

    def __init__(self):
        self.event_index = 1
        self.games = ["FIFA"] #bd fg
        self.tourney_styles = ["Bracket-SE", "Round Robin"] #BSE, BDE, RR
        self.events = pd.DataFrame({"Name":[], "Game":[], "Tournament":[]})
        self.players = pd.DataFrame({"Name":[], "Player_ID":[]})
        self.game_players = {}
        self.game_matches = {}

    def new_event(self,event_name, event_game, event_tournament):
        if event_game == "FIFA":
            event = FIFA(self.event_index, event_name, event_tournament)
        eventDf = pd.DataFrame({"Name":[event_name], "Game":[event_game], "Tournament":[event_tournament]},index=[self.event_index])
        self.events = pd.concat([self.events,eventDf])
        return event

    def update_game_players(self, game, game_players_pd):
        if game in self.game_players:
            self.game_players[game] = pd.concat([self.game_players,game_players_pd])
        else:
             self.game_players[game] = game_players_pd

    def update_game_matches(self, game, game_matches_pd):
        if game in self.game_matches:
            self.game_matches[game] = pd.concat([self.game_matches,game_matches_pd])
        else:
             self.game_matches[game] = game_matches_pd

    def get_events(self):
        return self.events

    def get_players(self):
        return self.players

    def get_game_players(self):
        return self.game_players

    def get_game_matches(self):
        return self.game_matches

class Event():

    def __init__(self, event_index, event_name, tournament_style):
        self.event_index = event_index
        self.event_name = event_name
        self.players = []
        self.max_players = None
        self.tournament_style = tournament_style
        self.locked = False


    def set_max_players(self, max_players):
        self.max_players = max_players

    def add_player(self, player):
        self.players.append(player)

    def add_players(self, players):
        for player in players:
            self.players.append(player)

    def set_tourney_style(self, tourney_style):
        self.tournament_style = tourney_style
    
    
class FIFA(Event):

    def __init__(self, event_index, event_name, tournament_style):
        super().__init__(event_index, event_name, tournament_style)
        self.tourney = None
        self.locked = False
        self.event_index = event_index
        self.players = pd.DataFrame({"Event_ID":[], "Name":[], "Team":[]})
        self.matches = pd.DataFrame({"Event_ID":[], "Home":[], "Away":[], "Winner":[]})
        self.matchup_count = 1

    def add_player(self, name, team): #use player id
        playerDf = pd.DataFrame({"Event_ID":[self.event_index], "Name":[name], "Team":[team]})
        self.players = pd.concat([self.players,playerDf])

    def get_players(self): #make in base class with possibility to override
        if not self.locked:
            self.locked = True
            return self.players
        else:
            print("Game is locked")

    def start_tournament(self):
        if self.locked:
            if self.tournament_style == "SEB":
                self.tourney = SEB(self.players["Name"].tolist())

    def get_first_round(self):
        if self.locked:
            matchups = self.tourney.get_round()
            for matchup in matchups:
                matchupDf = pd.DataFrame({"Event_ID":[self.event_index], "Home":[matchup[0]], "Away":[matchup[1]], "Winner":[None]},index=[self.matchup_count])
                self.matches = pd.concat([self.matches,matchupDf])
                self.matchup_count += 1
        return self.matches

    def get_next_round(self):
        if self.locked and None not in self.matches.loc[:,"Winner"].tolist():
            matchups = self.tourney.get_round()
            for matchup in matchups:
                print(matchup)
                matchupDf = pd.DataFrame({"Event_ID":[self.event_index], "Home":[matchup[0]], "Away":[matchup[1]], "Winner":[None]},index=[self.matchup_count])
                self.matches = pd.concat([self.matches,matchupDf])
                self.matchup_count += 1
        return self.matches #add winner to old matchups
        
    
    def input_score(self, matchup_ID, winner):
        self.matches.at[matchup_ID,"Winner"] = winner
        if winner == "Home":
            self.tourney.eliminate(self.matches.at[matchup_ID,"Away"])
        else:
            self.tourney.eliminate(self.matches.at[matchup_ID,"Home"])
        
    def randomize(self):
        self.tourney.randomize()

    def get_all_matchups(self):
        if self.tourney.over:
            return self.matches

class SEB:

    def __init__(self, players):
        self.players = players
        self.over = False

    def randomize(self):
        np.random.shuffle(self.players)
    
    def get_round(self):
        matchups = []
        count1 = 0
        count2 = 1
        for i in range(len(self.players)//2):
            matchups.append((self.players[count1],self.players[count2]))
            count1 += 2
            count2 += 2
        return matchups

    def eliminate(self, player):
        eliminated = self.players.pop(self.players.index(player))
        if len(self.players) == 1:
            print("Congrats to {:s}!".format(self.players[0]))
            self.over = True


class Player:

    def __init__(self, name):
        self.name = name
        self.age = None

    def set_age(self, age): #DOB?
        self.age = age



def example1():

    p1 = Player("Aaron")
    p1.set_age(22)
    p2 = Player("Xandra")
    p3 = Player("Tiffany")
    p4 = Player("Lucas")

    master = Master()
    event = master.new_event("Fifa", "FIFA", "SEB")
    event.add_player("Aaron", "Everton")
    event.add_player("Xandra", "Barca")
    event.add_player("Tiff", "Liverpool")
    event.add_player("Lucas", "Man U")
    players = event.get_players()
    event.start_tournament()
    event.randomize()
    event.get_first_round()
    master.update_game_players("FIFA", players)
    # print()
    # print(master.get_players())
    # print()
    # print(master.get_events())
    # print()
    # print(master.get_game_players()["FIFA"])
    # print()
    # print(event.matches)
    event.input_score(1,"Home")
    event.input_score(2,"Away")
    # print(event.matches)
    print()
    print(master.get_game_matches())
    event.get_next_round()

    #bug cuases None to go in dict and then cant concatenate
   # master.update_game_matches("FIFA", event.get_all_matchups())
    # print(event.matches)
    event.input_score(3, "Home")
    master.update_game_matches("FIFA", event.get_all_matchups())
    
    print()
    print(master.get_game_matches())

    return event

    

