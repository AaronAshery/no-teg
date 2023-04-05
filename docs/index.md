# Welcome to no-teg's documentation!


## Install

`pip install no-teg`

## Usage example: Create and run a basic single elimination tourament.
```python
from no_teg import *

p1 = Player("P1")
p2 = Player("P2")
p3 = Player("P1")
p4 = Player("P2")

MyGame = Game()
MyTourney = Single_Elimination(MyGame)
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
   :maxdepth: 2
   :caption: Contents:

   modules

* :ref:`genindex`
* :ref:`modindex`
```

