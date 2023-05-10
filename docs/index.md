# Welcome to no-teg's documentation!


# Install

`pip install no-teg`

# Usage example: Create and run a basic single elimination tourament.
```python
import no_teg as nt
from no_teg.tourneys import single_elimination

p1 = nt.Player("P1")
p2 = nt.Player("P2")
p3 = nt.Player("P3")
p4 = nt.Player("P4")

MyGame = nt.Game()
MyTourney = single_elimination.Single_Elimination(MyGame)
MyTourney.add_players([p1, p2, p3, p4])
MyTourney.start()
 
MyTourney.print_matchups()
1: P2 (A) vs P1 (H)
2: P4 (A) vs P3 (H)

# arguments are matchup_id, away_score, home_score, extra stats (see Further Examples)
MyTourney.input_result(1, 3, 2, [])
MyTourney.input_result(2, 0, 4, [])

MyTourney.print_results()
1: P2 (3) vs P1 (2)
2: P4 (0) vs P3 (4)

# P2 and P3 advance to the finals
MyTourney.print_matchups()
1: P2 (A) vs P1 (H)
2: P4 (A) vs P3 (H)
3: P2 (A) vs P3 (H)

# P2 wins the tournament!
MyTourney.input_result(3, 2, 1, [])
MyTourney.print_results()
1: P2 (3) vs P1 (2)
2: P4 (0) vs P3 (4)
3: P2 (2) vs P3 (1)

```

# Documentation

```eval_rst

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   modules

* :ref:`genindex`
* :ref:`modindex`
```

# Further Examples

## Players
```python

p5 = nt.Player("P5")
p5.get_name()
'P5'
p5.set_age(23)
```

## Team
```python

team1 = nt.Team("T1")
team1.add_players([p1, p2])
team1.get_name()
'T1'
```

## Game
```python

PingPong = nt.Game()
PingPong.set_name("Ping Pong")
PingPong.set_rec_players(4)
PingPong.set_rec_tourney(single_elimination.Single_Elimination)
PingPong.set_labels(["Away_Aces", "Home_Aces"])

#import a default game
from no_teg.games import fifa

fifa_game = fifa.FIFA()
fifa_tourney = single_elimination.Single_Elimination(fifa_game)


```


## Round-Robin Tournament
```python

from no_teg.tourneys import round_robin

RR = round_robin.Round_Robin(PingPong)
RR.add_players([p1, p2, p3, p4, p5])
RR.start()
RR.print_matchups()
1: P5 (A) vs P2 (H)
2: P4 (A) vs P3 (H)
3: P1 (A) vs P5 (H)
4: P3 (A) vs P2 (H)
5: P4 (A) vs P1 (H)
6: P5 (A) vs P3 (H)
7: P1 (A) vs P3 (H)
8: P2 (A) vs P4 (H)
9: P2 (A) vs P1 (H)
10: P4 (A) vs P5 (H)

```


## Single Elimination Tournament With Extra Stats
```python

RR2 = round_robin.Round_Robin(PingPong)
RR2.add_players([p1, p2, p3])
RR2.start()
RR2.print_matchups()
1: P3 (A) vs P2 (H)
2: P1 (A) vs P3 (H)
3: P2 (A) vs P1 (H)

# arguments are matchup_id, away_score, home_score, extra stats [Away_Aces, Home_Aces]
RR2.input_result(1, 7, 11, 3, 6)
RR2.input_result(2, 8, 11, 1, 5)
RR2.input_result(3, 11, 4, 9, 0)

```