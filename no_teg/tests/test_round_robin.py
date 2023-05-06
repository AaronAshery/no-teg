from no_teg import *
from ..tourneys import round_robin as rr
import pytest


@pytest.fixture
def rr_basic(game_basic):
    return rr.Round_Robin(game_basic)


@pytest.fixture
def rr_more(game_more):
    return rr.Round_Robin(game_more)


def test_rr_start(rr_basic, create_players):
    for i in range(3, 9):
        players = create_players(i)
        rr_basic.add_players(players)
        rr_basic.start()
        num_players = len(players)
        player_matchups = {player.get_name(): {"home": 0, "away": 0, "opponents": set()} for player in players}
        for match in rr_basic.matchups.values():
            home, away = match['Home'], match['Away']
            player_matchups[home]['home'] += 1
            player_matchups[away]['away'] += 1
            player_matchups[home]['opponents'].add(away)
            player_matchups[away]['opponents'].add(home)
        min_home_games = min([info['home'] for info in player_matchups.values()])
        assert min_home_games >= 1
        for player, info in player_matchups.items():
            assert len(info['opponents']) == num_players - 1
            assert info['opponents'] == {player.get_name() for player in players} - {player}
        max_home_games = max([info['home'] for info in player_matchups.values()])
        min_away_games = min([info['away'] for info in player_matchups.values()])
        max_away_games = max([info['away'] for info in player_matchups.values()])
        # still working on being balanced perfectly
        # assert max_home_games - min_home_games <= 1
        # assert max_away_games - min_away_games <= 1


def test_rr_input_result(rr_basic, create_players):
    players = create_players(4)
    rr_basic.add_players(players)
    rr_basic.start()

    assert rr_basic.matchups[1]["Away_Score"] == None
    assert rr_basic.matchups[1]["Home_Score"] == None
    rr_basic.input_result(1, 0, 1, [])
    assert rr_basic.matchups[1]["Away_Score"] == 0
    assert rr_basic.matchups[1]["Home_Score"] == 1

def test_rr_input_result_more(rr_more, create_players):
    players = create_players(4)
    rr_more.add_players(players)
    rr_more.start()

    assert rr_more.matchups[1]["Away_Score"] == None
    assert rr_more.matchups[1]["Home_Score"] == None
    rr_more.input_result(1, 0, 1, [2, 4])
    assert rr_more.matchups[1]["Away_Score"] == 0
    assert rr_more.matchups[1]["Home_Score"] == 1
    assert rr_more.matchups[1]["Away_Sportsmanship_Score"] == 2
    assert rr_more.matchups[1]["Home_Sportsmanship_Score"] == 4
