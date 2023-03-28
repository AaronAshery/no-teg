from no_teg import *
from unittest.mock import patch


### UNIT TESTS ###

TestTourney1 = Single_Elimination(FIFA())
p1 = Player("Aaron")
p2 = Player("Xandra")
p3 = Player("Lucas")
p4 = Player("Tiffany")


def test_Player_get_name():
    p1 = Player("Aaron")
    assert p1.get_name() == "Aaron"


def test_Player_set_age():
    p1.set_age(22)
    assert p1.age == 22


def test_Tourney_add_player():
    TestTourney2 = Single_Elimination(FIFA())
    p1 = Player("Aaron")
    TestTourney2.add_player(p1)
    assert TestTourney2.players == [p1]


def test_Tourney_add_players():
    TestTourney1.add_players([p1, p2, p3, p4])
    assert TestTourney1.players == [p1, p2, p3, p4]


# use a real error formula to check randomization
def test_Tourney_randomize_matchups():
    times_first = {p1: 0, p2: 0, p3: 0, p4: 0}
    times_in_order = 0  # 1/24 chance
    trials = 10000
    for i in range(trials):
        TestTourney1.randomize_matchups()
        times_first[TestTourney1.players[0]] += 1
        if TestTourney1.players == [p1, p2, p3, p4]:
            times_in_order += 1
    for player in TestTourney1.players:
        expected = trials / 4
        error = 0.2
        assert times_first[player] > expected - (expected * error) and times_first[player] < expected + (
            expected * error
        )
    expected = trials / 24  # 4!
    error = 0.2
    assert times_in_order > expected - (expected * error) and times_in_order < expected + (expected * error)


TestTourneyOrdered = Single_Elimination(FIFA())
p5 = Player("Aaron")
p6 = Player("Xandra")
p7 = Player("Lucas")
p8 = Player("Tiffany")


def test_SE_start():
    TestTourneyOrdered.add_players([p1, p2, p3, p4])
    TestTourneyOrdered.start()
    assert TestTourneyOrdered.matchups[1]["Away"] == "Xandra"
    assert TestTourneyOrdered.matchups[1]["Home"] == "Aaron"
    assert TestTourneyOrdered.matchups[1]["Home_Score"] == None
    assert TestTourneyOrdered.matchups[1]["Away_Score"] == None
    assert TestTourneyOrdered.matchups[1]["Next"] == 3
    assert TestTourneyOrdered.matchups[2]["Away"] == "Tiffany"
    assert TestTourneyOrdered.matchups[2]["Home"] == "Lucas"
    assert TestTourneyOrdered.matchups[3]["Home"] == None
    assert TestTourneyOrdered.matchups[3]["Away"] == None


def test_SE_get_matchups():
    assert TestTourneyOrdered.get_matchups() == TestTourneyOrdered.matchups


def test_SE_input_result():
    TestTourneyOrdered.input_result(1, 0, 1)
    assert TestTourneyOrdered.matchups[1]["Away_Score"] == 0
    assert TestTourneyOrdered.matchups[1]["Home_Score"] == 1
    assert TestTourneyOrdered.matchups[3]["Away"] == "Aaron"
    TestTourneyOrdered.input_result(2, 4, 2)
    assert TestTourneyOrdered.matchups[2]["Away_Score"] == 4
    assert TestTourneyOrdered.matchups[2]["Home_Score"] == 2
    assert TestTourneyOrdered.matchups[3]["Home"] == "Tiffany"
    assert TestTourneyOrdered.matchups[3]["Next"] == None
    assert TestTourneyOrdered.input_result(3, 1, 1) == False


myGame = Game()


def test_game():
    assert myGame.name == None
    assert myGame.rec_players == None
    assert myGame.rec_tourney == None
    assert myGame.labels == []


def test_game_set_name():
    myGame.set_name("Aaron's Awesome Game")
    assert myGame.name == "Aaron's Awesome Game"


def test_game_set_rec_players():
    myGame.set_rec_players(2)
    assert myGame.rec_players == 2


def test_game_set_rec_tourney():
    myGame.set_rec_tourney(Single_Elimination)
    assert myGame.rec_tourney == Single_Elimination


def test_game_set_labels():
    myGame.set_labels(["Total Jokers Used"])
    assert myGame.labels == ["Total Jokers Used"]


def test_game_get_labels():
    assert myGame.get_labels() == ["Total Jokers Used"]


### INTEGRATION TESTS ###


def test_SE_custom_game_tourney():
    MyGame = Game()
    MyGame.set_name("2v2 Basketball")
    MyGame.set_labels(["Home Fouls", "Away Fouls"])

    p1 = Player("Aaron")
    p2 = Player("Xandra")
    p3 = Player("Lucas")
    p4 = Player("Tiffany")
    p5 = Player("Raf")
    p6 = Player("Rhea")
    p7 = Player("Loki")
    p8 = Player("Richard")
    p9 = Player("Owen")
    p10 = Player("Saturn")
    p11 = Player("Mo")
    p12 = Player("Sergio")
    p13 = Player("Nick")
    p14 = Player("John")
    p15 = Player("Alex")
    p16 = Player("Ben")

    Team1 = Team("t1")
    Team1.add_player(p1)
    Team1.add_player(p2)
    Team2 = Team("t2")
    Team2.add_players([p3, p4])
    Team3 = Team("t3")
    Team3.add_players([p5, p6])
    Team4 = Team("t4")
    Team4.add_players([p7, p8])
    Team5 = Team("t5")
    Team5.add_player(p9)
    Team5.add_player(p10)
    Team6 = Team("t6")
    Team6.add_players([p11, p12])
    Team7 = Team("t7")
    Team7.add_players([p13, p14])
    Team8 = Team("t8")
    Team8.add_players([p15, p16])

    Tourney2v2 = Single_Elimination(MyGame)
    Tourney2v2.add_players([Team1, Team2, Team3, Team4, Team5, Team6, Team7, Team8])
    Tourney2v2.start()
    assert Tourney2v2.matchups[1]["Home"] == "t1"
    assert Tourney2v2.matchups[1]["Away"] == "t2"
    assert Tourney2v2.matchups[1]["Next"] == 5
    assert Tourney2v2.matchups[1]["Home Fouls"] == None
    Tourney2v2.input_result(1, 21, 14, [2, 4])
    Tourney2v2.input_result(2, 21, 20, [0, 1])
    Tourney2v2.input_result(3, 18, 21, [1, 1])
    Tourney2v2.input_result(4, 10, 21, [4, 3])
    assert Tourney2v2.matchups[5]["Away"] == "t2"
    assert Tourney2v2.matchups[5]["Home"] == "t4"
    assert Tourney2v2.matchups[5]["Next"] == 7
    assert Tourney2v2.matchups[1]["Home Fouls"] == 2
    Tourney2v2.input_result(5, 21, 19, [0, 0])
    Tourney2v2.input_result(6, 18, 21, [7, 9])
    assert Tourney2v2.matchups[7]["Home"] == "t7"
    assert Tourney2v2.matchups[7]["Away"] == "t2"
    assert Tourney2v2.matchups[7]["Next"] == None
    assert Tourney2v2.matchups[6]["Away Fouls"] == 9
    Tourney2v2.input_result(7, 21, 16, [3, 2])
    assert Tourney2v2.matchups[7]["Away_Score"] > Tourney2v2.matchups[7]["Home_Score"]


def test_RR_even():
    p1 = Player("Aaron")
    p2 = Player("Xandra")
    p3 = Player("Lucas")
    p4 = Player("Tiffany")
    MyGame = Game()
    TourneyRR = Round_Robin(MyGame)
    TourneyRR.add_players([p1, p2, p3, p4])
    TourneyRR.start()
    matchups = TourneyRR.get_matchups()
    assert len(matchups) == 6  # summation(num_players - 1) == 6
    # test everyone has same number of games
    games = {'Aaron': 0, 'Xandra': 0, 'Lucas': 0, 'Tiffany': 0}
    for v in matchups.values():
        games[v['Home']] += 1
        games[v['Away']] += 1
    assert games['Aaron'] == 3
    assert games['Xandra'] == 3
    assert games['Lucas'] == 3
    assert games['Tiffany'] == 3
    TourneyRR.input_result(1, 2, 1)
    print(matchups)
    assert matchups[1]["Away_Score"] == 2
    assert matchups[1]["Home_Score"] == 1


def test_RR_odd():
    p1 = Player("Aaron")
    p2 = Player("Xandra")
    p3 = Player("Lucas")
    p4 = Player("Tiffany")
    p5 = Player("Rhea")
    MyGame = Game()
    TourneyRR = Round_Robin(MyGame)
    TourneyRR.add_players([p1, p2, p3, p4, p5])
    TourneyRR.start()
    matchups = TourneyRR.get_matchups()
    TourneyRR.print_matchups()
    assert len(matchups) == 10  # summation(num_players - 1) == 1 + 2 + 3 + 4 == 10
    # test everyone has same number of games
    games = {'Aaron': 0, 'Xandra': 0, 'Lucas': 0, 'Tiffany': 0, 'Rhea': 0}
    for v in matchups.values():
        games[v['Home']] += 1
        games[v['Away']] += 1
    assert games['Aaron'] == 4
    assert games['Xandra'] == 4
    assert games['Lucas'] == 4
    assert games['Tiffany'] == 4
    assert games['Rhea'] == 4


####Test Classes####


class TestPlayer:
    def test_age(self):
        p1 = Player("Aaron")
        p1.set_age(22)
        assert p1.age == 22
