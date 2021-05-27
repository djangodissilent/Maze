from mazeHelpers import checkGoal, getSourceState, generateStates, printMaze, Move, showDemo, humanSolve, generateMaze, generateMazeRandom
from searchAlgos import solve

class Maze:
    '''
        A wraper around the search algorithms and the utillity fns
    '''
    def __init__(self, maze, checkGoal=checkGoal, generateStates=generateStates) -> None:
        self.maze = maze 
        self.checkGoal = checkGoal
        self.generateStates = generateStates
        self.startState = getSourceState(self.maze)

    def printMaze(self):
        return printMaze(self.maze)
    
    def solveAi(self, algo="astar", heuristic=None):
        '''solve maze by algorithm algo'''
        return solve(self.maze, self.startState, self.checkGoal, self.generateStates, algo=algo, heuristic=heuristic)

    def solveManual(self):
        ''' find path manually '''
        return humanSolve(self.maze)

    def animate(self, algo="astar"):
        ''' animate the path returned by algo '''
        return showDemo(self.maze, algo=algo)

    def Move(self, direction):
        mazeAndNewCost = Move(self.maze, direction)
        self.maze = mazeAndNewCost['maze']
        return mazeAndNewCost

sampleMaze = [
["v", "X", "X", "X", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", "X", " "],
[" ", "X", " ", "X", " "],
[" ", "X", "X", "X", "#"]
]

maze = generateMazeRandom(5)
m = Maze(maze)

# m.printMaze()
# print(m.solveAi("dfs"))
# print(m.solveAi("bfs"))
# print(m.solveAi("greedy"))
# print(m.solveAi("ucs"))
# print(m.solveAi("astar"))

# animate solution bath defualt is astar
m.animate(algo="ucs")

# solve by hand
# m.solveManual()