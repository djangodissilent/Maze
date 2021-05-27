import random


def checkGoal(maze, state):
    ''' check if the current state position is the goal '''
    pos = state.position
    return maze[pos[0]][pos[1]] == "#"


# return Euclidean distance to target from state position
def euclideanDistance(maze, state):
    '''
    retrun the Euclidean Distance distance between a state and the target
    '''
    targetPos = findTarget(maze)
    pos = state.position
    return ((pos[0] - targetPos[0])**2 + (pos[1] - targetPos[1])**2)**0.5


def findTarget(maze):
    '''find start and return source node'''
    pos = object
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] == "#":
                pos = (i, j)
                break

    return pos


import searchAlgos

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

    # shuffle directions
    # random.shuffle(newDirections)
    mazeln = maze.__len__()
    
    nStates = []
    for ndirection in filter(
            lambda nd: (0 <= nd[0] < mazeln) and
        (0 <= nd[1] < mazeln) and maze[nd[0]][nd[1]] != "X", newDirections):
        nStates.append(
            searchAlgos.stateNode(
                position=(ndirection[0], ndirection[1]),
                direction=ndirection[2],
                path=oldState.path + [ndirection[2]],
                cost=oldState.cost +
                1 if ndirection[2] == oldDirection else oldState.cost + 2))
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
    return searchAlgos.stateNode(position=pos, direction=maze[pos[0]][pos[1]])


# =============== Utils =========================
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


import colorama


def printMaze(maze, end="\n"):
    numberOfDashes = len(maze) * 4 + 1
    for row in maze:
        print("-" * numberOfDashes)
        print("|", end="")
        for c in row:
            if c == "X":
                print(
                    f"{colorama.Style.NORMAL} {colorama.Fore.LIGHTRED_EX}{c}{colorama.Fore.RESET}{colorama.Style.RESET_ALL} |",
                    end="")
            elif c == "#":
                print(
                    f"{colorama.Style.BRIGHT} {colorama.Fore.GREEN}{c}{colorama.Fore.RESET}{colorama.Style.RESET_ALL} |",
                    end="")
            elif c == "✔":
                print(
                    f"{colorama.Style.BRIGHT} {colorama.Fore.LIGHTBLUE_EX}{c}{colorama.Fore.RESET}{colorama.Style.RESET_ALL} |",
                    end="")
            elif c in ["<", ">", "^", "v"]:
                print(
                    f"{colorama.Style.BRIGHT} {colorama.Fore.BLUE}{c}{colorama.Fore.RESET}{colorama.Style.RESET_ALL} |",
                    end="")
            else:
                print(f" {c} |", end="")

        print()
    print("-" * numberOfDashes, end=end)


from os import system, name as _name
from time import sleep


def showDemo(maze, algo="dfs"):
    ''' animate the solution to the console '''

    # clear the prompt based on the OS supports [windows - linux]
    cls = lambda: system("cls") if _name == "nt" else system("clear")
    cls()

    print(10 * "*", f"Starting Demo for {algo.upper()}", 10 * "*")
    sleep(1)
    startState = getSourceState(maze)

    # dont permutate the original maze
    maze = deepcopy(maze)
    sol = searchAlgos.solve(maze,
                            startState,
                            checkGoal,
                            generateStates,
                            algo=algo,
                            heuristic=None)
    printMaze(maze)
    if "Fail" in sol: 
        cls()
        print(sol['Fail'])
        sleep(2)
        return
    visMaze = deepcopy(maze)
    sleep(1)
    cls()
    print("relaxing states ..")
    sleep(1)

    for state in sol['visited']:
        cls()
        pos = state.position
        visMaze[pos[0]][pos[1]] = "✔"
        printMaze(visMaze)
        sleep(0.05)

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
        sleep(0.3)
        cls()
    printMaze(maze)
    for x in sol:
        if x != "visited":
            print(x, ":", sol[x])


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
            print("Game Over")
            return

        else:
            chosenState = [
                state for state in states if state.direction == direction
            ][0]
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


# Maze generation using Dfs
def generateMaze(n):
    ''' 
    returns a generated new random maze
    
    '''

    maze = []
    # generates random position
    randPos = lambda: (random.randrange(n), random.randrange(n))

    # make an empty maze
    for _ in range(n):
        maze.append([" " for k in range(n)])

    # get different random positions for start and end
    s, t = (0, 0), (0, 0)
    while (s == t):
        s = randPos()
        t = randPos()

    # set the start and end at random
    maze[s[0]][s[1]] = random.choice(["<", ">", "v", "^"])
    maze[t[0]][t[1]] = "#"

    # save target direction
    carDirection = maze[s[0]][s[1]]

    # run DFS and save the path to generate the maze
    initial_state = getSourceState(maze)
    sol = searchAlgos.solve(maze,
                            initial_state,
                            checkGoal,
                            generateStates,
                            algo="dfs",
                            heuristic=None)

    # make all the maze walls (unraechable)
    for l in maze:
        for i in range(len(l)):
            if l[i] == " ": l[i] = "X"

    # clear bfs path to make the maze
    startPos = s
    maze[startPos[0]][startPos[1]] = " "
    for direction in sol["path"]:
        if direction == ">": startPos = (startPos[0], startPos[1] + 1)
        elif direction == "^": startPos = (startPos[0] - 1, startPos[1])
        elif direction == "<": startPos = (startPos[0], startPos[1] - 1)
        else: startPos = (startPos[0] + 1, startPos[1])
        maze[startPos[0]][startPos[1]] = " "

    # put the target and the car back
    maze[s[0]][s[1]] = carDirection
    maze[t[0]][t[1]] = "#"

    return maze


def generateMazeRandom(n):
    nMaze = [[(random.choice([" ", " ", "X"])) for i in range(n)]
             for j in range(n)]
    # get different random positions for start and end
    s, t = (0, 0), (0, 0)
    randPos = lambda: (random.randrange(n), random.randrange(n))

    while (s == t):
        s = randPos()
        t = randPos()

    nMaze[s[0]][s[1]] = random.choice(["<", ">", "v", "^"])
    nMaze[t[0]][t[1]] = "#"
    return nMaze

# TODO
def displayMaze(maze):
    '''  Display maze as gui '''
    pass