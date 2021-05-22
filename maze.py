from mazeHelpers import checkGoal, getSourceState, generateStates, printMaze, Move, showDemo, humanSolve
from searchAlgos import solve

class Maze:
    def __init__(self, maze, checkGoal=checkGoal, generateStates=generateStates, heuristic=None) -> None:
        self.maze = maze
        self.checkGoal = checkGoal
        self.generateStates = generateStates
        self.heuristic = heuristic
        self.startState = getSourceState(maze)

    def printMaze(self):
        return printMaze(self.maze)
    
    def solveAi(self, algo="astar"):
        return solve(maze, self.startState, self.checkGoal, self.generateStates, algo=algo, heuristic=self.heuristic)

    def solveManual(self):
        return humanSolve(self.maze)

    def animate(self, algo="astar"):
        return showDemo(self.maze, algo=algo)

    def Move(self, direction):
        mazeAndNewCost = Move(self.maze, direction)
        self.maze = mazeAndNewCost['maze']
        return mazeAndNewCost


# maze = generateMaze()
maze = [
["v", "X", "X", "X", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", "X", " "],
[" ", "X", " ", "X", " "],
[" ", "X", "X", "X", "#"]
]


m = Maze(maze)
print(m.solveAi("dfs"))
print(m.solveAi("bfs"))
print(m.solveAi("greedy"))
print(m.solveAi("ucs"))
print(m.solveAi("astar"))

# animate solution bath defualt is astar
m.animate()

# solve by hand
# m.solveManual()