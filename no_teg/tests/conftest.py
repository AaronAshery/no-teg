import pytest
from no_teg import Player, Game


@pytest.fixture
def create_players():
    def _create_players(num_players):
        return [Player(f"Player {i}") for i in range(1, num_players + 1)]

    return _create_players


@pytest.fixture
def game_basic():
    game = Game()
    game.set_name("Basic Game")
    return game


@pytest.fixture
def game_more():
    game = Game()
    game.set_name("Complex Game")
    game.set_labels(["Away_Sportsmanship_Score", "Home_Sportsmanship_Score"])
    return game
