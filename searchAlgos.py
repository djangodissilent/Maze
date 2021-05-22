from collections import deque
from heapq import heapify, heappop, heappush

class stateNode(object):
    def __init__(self, position, direction, path=[], cost=0) -> None:
        super().__init__()
        self.position = position
        self.direction = direction
        self.path = path
        self.cost = cost

    def __lt__(self, other) -> bool:
        return self.cost < other.cost

    def __hash__(self) -> int:
        return hash((self.position, self.direction))

    def __eq__(self, other) -> bool:
        return (self.position, self.direction) == (other.position, other.direction)

    def __str__(self) -> str:
        return f"position: {self.position}\ndirection: {self.direction}\ncost: {self.cost}\npath: {self.path}\n"

from mazeHelpers import euclideanDistance

def solve(maze, initail_state, is_goal, next_state, algo="astar", heuristic=None):
    algos = {"astar": astar, "dfs": dfs, "bfs": bfs, "ucs":ucs, "greedy": greedy}
    if heuristic:
        return algos[algo](maze, initail_state, is_goal, next_state, heuristic) if algo in algos else  {"Fail": "cant reach goal state"}
    return algos[algo](maze, initail_state, is_goal, next_state) if algo in algos else  {"Fail": "cant reach goal state"}

def bfs(maze, initail_state, is_goal, generateStates):
    # fringe is now a doubly linkedList
    fringe, visited = deque([]), {}
    fringe.append(stateNode(initail_state.position, initail_state.direction))
    while fringe.__len__():
        current_state = fringe.popleft()
        if is_goal(maze, current_state):
            return { "path": current_state.path, "relaxed":len(visited), "cost": current_state.cost}
        if current_state in visited:
            continue
        else:
            visited[current_state] = True
        for newState in generateStates(maze, current_state):
            fringe.append(newState)

    return {"Fail": "cant reach goal state"}

def dfs(maze, initail_state, is_goal, generateStates):
    fringe, visited = [], {}
    fringe.append(stateNode(initail_state.position, initail_state.direction))

    while fringe.__len__():
        current_state = fringe.pop()
        if is_goal(maze, current_state):
            return { "path": current_state.path, "relaxed":len(visited), "cost": current_state.cost}
        if current_state in visited:
            continue
        else:
            visited[current_state] = True
        for newState in generateStates(maze, current_state):
            fringe.append(newState)
            
    return {"Fail": "cant reach goal state"}

def ucs(maze, initail_state, is_goal, generateStates):
    '''Minimize on the Cost (defualt)'''
    return bestFirst(maze, initail_state, is_goal, generateStates)

def greedy(maze, initail_state, is_goal, generateStates, heuristic=euclideanDistance):
    '''Minimize on the heuristic'''
    f = lambda self, other : heuristic(maze, self) < heuristic(maze, other) 
    return bestFirst(maze, initail_state, is_goal, generateStates, f, heuristic=euclideanDistance)

def astar(maze, initail_state, is_goal, generateStates, heuristic=euclideanDistance):
    '''Minimize on both'''
    f = lambda self, other: self.cost + heuristic(maze, self) < other.cost + heuristic(maze, other)  
    return bestFirst(maze, initail_state, is_goal, generateStates, f, heuristic=euclideanDistance)

def bestFirst(maze, initail_state, is_goal, generateStates, f = lambda self, other: self.cost < other.cost, heuristic=euclideanDistance):
    fringe, visited = [], {}
    fringe.append(stateNode(initail_state.position, initail_state.direction))
    heapify(fringe)
    # override the defualt dunderMethod at runtime 
    stateNode.__lt__ = f
    while fringe.__len__():
        # minimize from heuristic pov and return the state
        current_state = heappop(fringe)
        if is_goal(maze, current_state):
            return { "path": current_state.path, "relaxed":len(visited), 'cost': current_state.cost}
        if current_state in visited:
            continue
        else:
            visited[current_state] = True
        for newState in generateStates(maze, current_state):
            heappush(fringe, newState)
    return {"Fail": "cant reach goal state"}