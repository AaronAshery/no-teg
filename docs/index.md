# Welcome to no-teg's documentation!


## Install

`pip install no-teg`

## Usage example: Create and run a basic single elimination tourament.
```python
import no_teg as nt

p1 = nt.Player("P1")
p2 = nt.Player("P2")
p3 = nt.Player("P1")
p4 = nt.Player("P2")

MyGame = nt.Game()
MyTourney = nt.Single_Elimination(MyGame)
MyTourney.add_players([p1, p2, p3, p4])
MyTourney.start()
 
MyTourney.print_matchups()
1: P2 (A) vs P1 (H)
2: P4 (A) vs P3 (H)

# arguments are matchup_id, away_score, home_score
MyTourney.input_result(1, 3, 2)
MyTourney.input_result(2, 0, 4)

MyTourney.print_results()
1: P2 (3) vs P1 (2)
2: P4 (0) vs P3 (4)

#P2 and P3 advance to the finals
MyTourney.print_matchups()
1: P2 (A) vs P1 (H)
2: P4 (A) vs P3 (H)
3: P2 (A) vs P3 (H)

#P2 wins the tournament!
MyTourney.input_result(3, 2, 1)
MyTourney.print_results()
1: P2 (3) vs P1 (2)
2: P4 (0) vs P3 (4)
3: P2 (2) vs P3 (1)

```

## Documentation

```eval_rst

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   modules

* :ref:`genindex`
* :ref:`modindex`
```

## Further Examples
```python
import no_teg as nt
```

# Players
```python

p1 = nt.Player("P1")
p1.get_name()
'P1'
p1.set_age(23)

p2 = nt.Player()
p2.set_name("P2")
```

# Team
```python

team1 = nt.Team("T1")
team1.add_players([p1, p2])
team1.get_name()
'T1'
```

# Game
```python

PingPong = nt.Game()
PingPong.set_name("Ping Pong")
PingPong.set_rec_players(4)
PingPong.set_rec_tourney(nt.RoundRobin)
PingPong.set_labels(["Aces"])
```


# Round-Robin Tournament
```python
#initiate more players
p3 = nt.Player("P3")
p4 = nt.Player("P4")

RR = nt.Round_Robin(PingPong)
RR.add_players([p1, p2, p3, p4])
RR.start()
RR.print_matchups()
1: P4 (A) vs P1 (H)
2: P3 (A) vs P2 (H)
3: P3 (A) vs P1 (H)
4: P2 (A) vs P4 (H)
5: P2 (A) vs P1 (H)
6: P4 (A) vs P3 (H)

```