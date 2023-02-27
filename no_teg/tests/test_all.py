from no_teg import *
from unittest.mock import patch

def test_get_name():
    p1 = Player("Aaron")
    assert p1.get_name() == "Aaron"