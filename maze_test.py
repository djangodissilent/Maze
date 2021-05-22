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

    def test_addition(self):
        assert m.solveAi("dfs") == resDfs
        assert m.solveAi("bfs") == resBfs
        assert m.solveAi("greedy") == resGreedy
        assert m.solveAi("ucs") == resUcs
        assert m.solveAi("astar") == resAstar

resDfs = {'path': ['v', 'v', 'v', 'v', '^', '^', '^', '>', 'v', '<', '>', '^', '>', 'v', 'v', '^', '<', '>', '^', '>', '>', 'v', 'v', 'v'], 'relaxed': 28, 'cost': 38}
resBfs ={'path': ['v', '>', '>', '>', '>', 'v', 'v', 'v'], 'relaxed': 33, 'cost': 10}
resGreedy = {'path': ['v', '>', '>', '>', '>', 'v', 'v', 'v'], 'relaxed': 31, 'cost': 10}
resUcs = {'path': ['v', '>', '>', '>', '>', 'v', 'v', 'v'], 'relaxed': 31, 'cost': 10}
resAstar = {'path': ['v', '>', '>', '>', '>', 'v', 'v', 'v'], 'relaxed': 31, 'cost': 10}