from mazeHelpers import checkGoal, getSourceState, generateStates, printMaze, Move, showDemo
from searchAlgos import solve

def humanSolve(maze):
    cost = 0
    while 1:
        printMaze(maze)
        source = getSourceState(maze)
        states = generateStates(maze, source)
        directions = [state.direction for state in states]
        print("available actions: " + ", ".join(directions))
        direction = input("Enter Direction: ")
        if direction not in directions:
            print("Game Over"); return

        else:
            chosenState = [state for state in states if state.direction == direction][0]
            if checkGoal(maze, chosenState):
                mazeAndCost = Move(maze, direction)
                maze = mazeAndCost['maze']
                cost += mazeAndCost['cost']
                printMaze(mazeAndCost['maze'])
                print(f"You Win\nCost: {cost}")
                return
            mazeAndCost = Move(maze, direction)
            maze = mazeAndCost['maze']
            cost += mazeAndCost['cost']
            printMaze(mazeAndCost['maze'])


def computerSolve(maze, algo="astar", heuristic=None, verbose=False):
    '''
    prints solition after solving maze by algorithms algo
    set verobose to show maze after each step of the solution
    '''
    printMaze(maze)
    # get the start state
    initial_state = getSourceState(maze)
    solution = solve(maze, initial_state, checkGoal, generateStates, heuristic=heuristic, algo=algo)
    print(f"< {algo} >")
    for entry in solution:
        print(entry,":", solution[entry])
        
    if verbose: 
        oldMaze = maze
        printMaze(oldMaze)
        for  direction in solution['path']:
            printMaze(oldMaze:=Move(oldMaze, direction)['maze'])

maze = [
["v", "X", "X", "X", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", "X", " "],
[" ", "X", " ", "X", " "],
[" ", "X", "X", "X", "#"]
]


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

m = Maze(maze)
print(m.solveAi("dfs"))
print(m.solveAi("bfs"))
print(m.solveAi("greedy"))
print(m.solveAi("ucs"))
print(m.solveAi("astar"))
# m.solveManual()

# animate solution bath defualt is astar
m.animate()