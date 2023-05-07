from no_teg import *
from ..tourneys import single_elimination as se
import pytest


@pytest.fixture
def se_basic(game_basic):
    return se.Single_Elimination(game_basic)


@pytest.fixture
def se_more(game_more):
    return se.Single_Elimination(game_more)


def test_fixtures(se_basic, se_more, create_players):
    assert isinstance(se_basic, se.Single_Elimination), "se_basic fixture is not working correctly"
    assert isinstance(se_more, se.Single_Elimination), "se_more fixture is not working correctly"
    players = create_players(4)
    print("Players:", players)
    assert len(players) == 4
    for player in players:
        assert isinstance(player, Player), "Players fixture is not working correctly"


def test_se_add_player(se_basic, create_players):
    assert len(se_basic.players) == 0
    players = create_players(1)
    se_basic.add_player(players[0])
    assert len(se_basic.players) == 1


def test_se_add_players(se_basic, create_players):
    assert len(se_basic.players) == 0
    players = create_players(4)
    se_basic.add_players(players)
    assert len(se_basic.players) == 4


def test_se_start_no_byes(se_basic, create_players):
    players = create_players(4)
    se_basic.add_players(players)
    se_basic.start()
    assert len(se_basic.matchups) == 3
    assert len(se_basic.matchups[1]) == 5
    assert se_basic.matchups[1]["Away"] != None
    assert se_basic.matchups[1]["Home"] != None
    assert se_basic.matchups[1]["Away_Score"] == None
    assert se_basic.matchups[1]["Home_Score"] == None
    assert se_basic.matchups[1]["Next"] == 3
    assert se_basic.matchups[2]["Away"] != None
    assert se_basic.matchups[2]["Home"] != None
    assert se_basic.matchups[1]["Next"] == 3
    assert se_basic.matchups[3]["Away"] == None
    assert se_basic.matchups[3]["Home"] == None


def test_se_get_matchups_no_byes(se_basic, create_players):
    players = create_players(4)
    se_basic.add_players(players)
    se_basic.start()
    assert se_basic.get_matchups() == se_basic.matchups


def test_se_input_result_no_byes(se_basic, create_players):
    players = create_players(4)
    se_basic.add_players(players)
    se_basic.start()
    # (matchup_id, away_score, home_score, [extra_stats])
    se_basic.input_result(1, 0, 1, [])
    assert se_basic.matchups[1]["Away_Score"] == 0
    assert se_basic.matchups[1]["Home_Score"] == 1
    assert len(se_basic.matchups[1]) == 5

    se_basic.input_result(2, 4, 2, [])
    assert se_basic.matchups[2]["Away_Score"] == 4
    assert se_basic.matchups[2]["Home_Score"] == 2

    assert se_basic.matchups[3]["Away"] == se_basic.matchups[1]["Home"]
    assert se_basic.matchups[3]["Home"] == se_basic.matchups[2]["Away"]

    assert se_basic.input_result(3, 1, 1, []) == False
    assert se_basic.matchups[3]["Away_Score"] == None
    assert se_basic.matchups[3]["Home_Score"] == None


def test_se_start_byes(se_basic, create_players):
    players = create_players(6)
    se_basic.add_players(players)
    se_basic.start()
    assert len(se_basic.matchups) == 7
    assert se_basic.matchups[1]["Away"] != None
    assert se_basic.matchups[1]["Home"] != None
    assert se_basic.matchups[1]["Away_Score"] == None
    assert se_basic.matchups[1]["Home_Score"] == None
    assert se_basic.matchups[1]["Next"] == 5

    assert se_basic.matchups[3]["Away"] == "Bye"
    assert se_basic.matchups[3]["Home"] != "Bye"
    assert se_basic.matchups[3]["Away_Score"] == 0
    assert se_basic.matchups[3]["Home_Score"] == 3

    assert se_basic.matchups[4]["Away"] == "Bye"
    assert se_basic.matchups[4]["Home"] != "Bye"
    assert se_basic.matchups[4]["Away_Score"] == 0
    assert se_basic.matchups[4]["Home_Score"] == 3

    assert se_basic.matchups[3]["Next"] == se_basic.matchups[4]["Next"]
    next = se_basic.matchups[3]["Next"]
    assert se_basic.matchups[next]["Away"] != None
    assert se_basic.matchups[next]["Home"] != None
    assert se_basic.matchups[next]["Away_Score"] == None
    assert se_basic.matchups[next]["Home_Score"] == None


def test_se_input_result_byes(se_basic, create_players):
    players = create_players(6)
    se_basic.add_players(players)
    se_basic.start()
    se_basic.input_result(1, 0, 1, [])
    assert se_basic.matchups[1]["Away_Score"] == 0
    assert se_basic.matchups[1]["Home_Score"] == 1
    next = se_basic.matchups[1]["Next"]
    assert len(se_basic.matchups[1]) == 5
    assert se_basic.matchups[next]["Away"] == se_basic.matchups[1]["Home"]


def test_se_start_more(se_more, create_players):
    players = create_players(4)
    se_more.add_players(players)
    se_more.start()
    assert len(se_more.matchups[1]) == 7
    assert se_more.matchups[1]["Away"] != None
    assert se_more.matchups[1]["Home"] != None
    assert se_more.matchups[1]["Away_Score"] == None
    assert se_more.matchups[1]["Home_Score"] == None
    assert se_more.matchups[1]["Next"] == 3
    assert se_more.matchups[1]["Home_Sportsmanship_Score"] == None
    assert se_more.matchups[1]["Away_Sportsmanship_Score"] == None


def test_se_input_result_more(se_more, create_players):
    players = create_players(4)
    se_more.add_players(players)
    se_more.start()
    se_more.input_result(1, 0, 1, [2, 4])
    assert se_more.matchups[1]["Away_Score"] == 0
    assert se_more.matchups[1]["Home_Score"] == 1
    assert se_more.matchups[1]["Away_Sportsmanship_Score"] == 2
    assert se_more.matchups[1]["Home_Sportsmanship_Score"] == 4
    assert len(se_more.matchups[1]) == 7
    next = se_more.matchups[1]["Next"]
    assert se_more.matchups[next]["Away"] == se_more.matchups[1]["Home"]
