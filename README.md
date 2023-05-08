# no-teg
A library for running tournaments

![license](https://img.shields.io/github/license/aaronashery/no-teg)
![issues](https://img.shields.io/github/issues/AaronAshery/no-teg)
[![Build Status](https://github.com/ColumbiaOSS/example-project-python/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/AaronAshery/no-teg/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/AaronAshery/no-teg/branch/main/graph/badge.svg)](https://codecov.io/gh/ColumbiaOSS/example-project-python)
[![PyPI](https://img.shields.io/pypi/v/no-teg)](https://pypi.org/project/no-teg/)
[![Docs](https://img.shields.io/readthedocs/no-teg.svg)](https://no-teg.readthedocs.io/en/latest/)

## Overview
'no-teg' (get-on backwards) is a library for running tournaments. In the beginning it will be simple i.e. setting up and advancing through different tournament styles. Eventually if things go smoothly the library will also compute data on the tournaments and players. Being open-source, I hope that people will add tournament styles and different analysis that are dependent on different games.

## Install:

`pip install no-teg`
 
## Usage example: Create and run a basic single elimination tourament.
```python
import no_teg as nt
from no_teg.tourneys import Single_Elimination

p1 = nt.Player("P1")
p2 = nt.Player("P2")
p3 = nt.Player("P3")
p4 = nt.Player("P4")

MyGame = nt.Game()
MyTourney = Single_Elimination.Single_Elimination(MyGame)
MyTourney.add_players([p1, p2, p3, p4])
MyTourney.start()
 
MyTourney.print_matchups()
1: P2 (A) vs P1 (H)
2: P4 (A) vs P3 (H)

# arguments are matchup_id, away_score, home_score, extra stats (see Further Examples on docs page)
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


## Available Tourneys
- Single_Elimination
- Round_Robin

 
## Makefile commands:
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make format`: autoformat this library using `black`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information
- `make dist`: package library for distribution
