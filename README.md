# no-teg
A library for running tournaments

![license](https://img.shields.io/github/license/aaronashery/no-teg)
![issues](https://img.shields.io/github/issues/AaronAshery/no-teg)
[![Build Status](https://github.com/ColumbiaOSS/example-project-python/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/AaronAshery/no-teg/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/AaronAshery/no-teg/branch/main/graph/badge.svg)](https://codecov.io/gh/ColumbiaOSS/example-project-python)

## Overview
'no-teg' (get-on backwards) is a library for running tournaments. In the beginning it will be simple i.e. setting up and advancing through different tournament styles. Eventually if things go smoothly the library will also compute data on the tournaments and players. Being open-source, I hope that people will add tournament styles and different analysis that are dependent on different games.


Makefile commands:
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make format`: autoformat this library using `black`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information
- `make dist`: package library for distribution