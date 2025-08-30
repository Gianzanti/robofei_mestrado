import pytest

from robofei import greet


def test_greet_world():
    assert greet("world") == "Hello, world from robofei!"

def test_greet_custom():
    assert greet("Fabio") == "Hello, Fabio from robofei!"