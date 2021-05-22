class stateNode(object):
    def __init__(self, position, direction, path=[], cost=0) -> None:
        self.position = position
        self.direction = direction
        self.path = path
        self.cost = cost

    def __lt__(self, other) -> bool:
        return self.cost < other.cost

    def __hash__(self) -> int:
        return hash((self.position, self.direction))

    def __eq__(self, other) -> bool:
        return (self.position, self.direction) == (other.position,
                                                   other.direction)

    def __str__(self) -> str:
        return f"position: {self.position}\ndirection: {self.direction}\ncost: {self.cost}\npath: {self.path}\n"

# TODO
def generateMaze(n):
    ''' generate random new maze & return the generated maze'''
    pass

# TODO
def displayMaze(maze):
    '''  Display maze to console or through a gui '''
    pass

def checkGoal(maze, state):
    ''' check if the current state position is the goal '''
    pos = state.position
    return maze[pos[0]][pos[1]] == "#"


def generateStates(maze, oldState):
    '''
    Generates new states based on the current state and the maze
    '''
    oldPos = oldState.position
    oldDirection = oldState.direction
    # RIGHT _ UP _ LEFT _ DOWN
    newDirections = [(oldPos[0], oldPos[1] + 1, ">"),
                     (oldPos[0] - 1, oldPos[1], "^"),
                     (oldPos[0], oldPos[1] - 1, "<"),
                     (oldPos[0] + 1, oldPos[1], "v")]
    mazeln = maze.__len__()

    nStates = []
    for ndirection in filter(
            lambda nd: (0 <= nd[0] < mazeln) and
        (0 <= nd[1] < mazeln) and maze[nd[0]][nd[1]] != "X", newDirections):
        nStates.append(
            stateNode(position=(ndirection[0], ndirection[1]),
                      direction=ndirection[2],
                      path=oldState.path + [ndirection[2]],
                      cost=oldState.cost +
                      1 if ndirection[2] == oldDirection else oldState.cost +
                      2))

    return nStates

def getSourceState(maze):
    '''find start and return source node'''
    pos = object
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] in ["<", ">", "^", "v"]:
                pos = (i, j)
                break
    # make the state with the returned position
    return stateNode(position=pos, direction=maze[pos[0]][pos[1]])

def findTarget(maze):
    '''find start and return source node'''
    pos = object
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j]  == "#":
                pos = (i, j)
                break

    return pos

# return Euclidean distance to target from state position
def euclideanDistance(maze, state):
    '''
    retrun the Euclidean Distance distance between a state and the target
    '''
    targetPos = findTarget(maze)
    pos = state.position
    return ((pos[0] - targetPos[0])**2 + (pos[1] - targetPos[1])**2)**0.5


# Utils
from copy import deepcopy 

def Move(oldMaze, direction):
    '''
    returns a maze moved in a given direction and move cost
    based on the old state
    dosent change given maze 
    '''
    maze = deepcopy(oldMaze)
    oldState = getSourceState(maze)
    reachableStates = generateStates(maze, oldState)
    canMove = direction in [state.direction for state in reachableStates]

    cost = 0
    if canMove:
        cost = cost + 1 if direction == oldState.direction else cost + 2
        newState = [
            state for state in reachableStates if state.direction == direction
        ][0]
        newPos = newState.position
        oldPos = oldState.position
        maze[oldPos[0]][oldPos[1]], maze[newPos[0]][newPos[1]] = " ", direction

        return {"maze": maze, 'cost': cost}
    else:
        return "Failure: Can't Move There"


def printMaze(maze, end="\n"):
    numberOfDashes = 21
    for row in maze:
        print("-" * numberOfDashes)
        print("|", end="")
        for c in row:
            print(f" {c} |", end="")

        print()
    print("-" * numberOfDashes, end=end)



from os import system, name as _name
from time import sleep

from searchAlgos import solve

def showDemo(maze, algo="dfs"):
    ''' animate the solution to the console '''

    # clear the prompt based on the OS supports [windows - linux]
    cls = lambda: system("cls") if _name == "nt" else system("clear")
    cls()

    print(10*"*", f"Starting Demo for {algo.upper()}", 10*"*")
    sleep(1)
    startState = getSourceState(maze)

    # dont permutate the original maze
    maze = deepcopy(maze)
    sol = solve(maze, startState, checkGoal, generateStates, algo=algo, heuristic=None)
    printMaze(maze)
    for x in sol:
        print(x, ":", sol[x])

    sleep(2)
    cls()
    print("Replicating Best Rout...")
    sleep(1)
    cls()
    cost = 0
    for direction in sol['path']:
        newMazeAndCost = Move(maze, direction)
        cost += newMazeAndCost['cost']
        maze = newMazeAndCost['maze']
        printMaze(maze, end=" ")
        print(f"cost: {cost}")
        sleep(0.7)
        cls()

    printMaze(maze)

def humanSolve(maze):
    ''' solve the maze interactivly by a human'''
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

