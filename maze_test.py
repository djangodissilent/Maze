"""
Unit tests for the Maze class
"""

from maze import Maze

testMaze = [
["v", "X", "X", "X", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", "X", " "],
[" ", "X", " ", "X", " "],
[" ", "X", "X", "X", "#"]
]


m = Maze(testMaze)

class TestMaze:

    def test_algos(self):
        assert m.solveAi("ucs")['cost'] == resUcs['cost']
        assert m.solveAi("ucs")['path'] == resUcs['path']
        assert m.solveAi("astar")['cost'] == resAstar['cost']
        assert m.solveAi("astar")['path'] == resAstar['path']

resUcs = {'path': ['v', '>', '>', '>', '>', 'v', 'v', 'v'], 'relaxed': 31, 'cost': 10}
resAstar = {'path': ['v', '>', '>', '>', '>', 'v', 'v', 'v'], 'relaxed': 31, 'cost': 10}