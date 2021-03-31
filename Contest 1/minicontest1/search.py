# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]
"""
def depthFirstSearch(problem):

    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    "
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    start_state = problem.getStartState()   # Getting the start state of the Problem
    open_stack = util.Stack()   # Defining the stack for OPEN

    open_stack.push((start_state, [], 0))    #Pushing the start state, action (none) and cost (0 since first node) on the stack
    closed_list = []    # Keeping track of visited nodes

    (state, NextDir, Cost) = open_stack.pop() #Popping the first entry of the OPEN
    closed_list.append(state)    #Adding the base node to the list of visited nodes

    while not problem.isGoalState(state):  # Keep exploring if we haven't reached goal state
        #print(state)
        next_nodes = problem.getSuccessors(state) # Getting the child nodes
        for node in next_nodes:
            n1 = node[0]    # Node
            d1 = node[1]   # Direction of node
            c1 = node[2]    # Cost of Node
            if ((problem.isGoalState(n1)) or (not n1 in closed_list)):
            #Checking if the node is the goal state or has been visited already
                open_stack.push((n1, NextDir + [d1], Cost + c1))
                closed_list.append(n1) #Adding the node to visited node lists
        (state, NextDir, Cost) = open_stack.pop()      #Pop the next node on the stack
    return NextDir

    util.raiseNotDefined()
"""

def depthFirstSearch(problem):
    """
    Second attempt at DFS. The first implementation works fine for 4/5 test cases.
    The mistake is probably terminating the search when we reach goal node, rather than
    when the goal node is popped from the stack.
    """
    Open_stack = util.Stack() #Initialize OPEN as stack
    closed_list = []    # Keeping track of visited nodes
    start_state = problem.getStartState()   # Getting the start state of the Problem
    Open_stack.push([(start_state, [], 0)])

    while not Open_stack.isEmpty(): #Keep searching until OPEN is not empty (Differs from the previous implementation)
        search_p = Open_stack.pop()  #The path that we will consider for searching is popped from the Stack

        #We select the current node from the search path
        c_node = search_p[-1][0] # This will provide with the corrdinates of the last element in the search path

        #Now, we check if the current node is the goal state
        if problem.isGoalState(c_node):
            #if true, we return the directions for the pacman to follow
            final_path = [p[1] for p in search_p] #to remove the first entry from the result
            return final_path[1:]

        if c_node not in closed_list:
            for next_node in problem.getSuccessors(c_node): #this gives the successors of the current node
                if next_node[0] not in closed_list: #Checking whether it's been visited already
                    updated_path = search_p[:] #Copying all the tuples currently stored in the Search Path
                    updated_path.append(next_node)  #this updates the current path
                    Open_stack.push(updated_path)
            closed_list.append(c_node) #Updating closed list to indicate that current node has been visited
    return False    #Incase the search doesn't find goal state


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()   # Getting the start state of the Problem
    open_queue = util.Queue()   # Defining the queue for OPEN

    open_queue.push((start_state, [], 0))    #Pushing the start state, action (none) and cost (0 since first node) on the stack
    closed_list = []    # Keeping track of visited nodes

    (state, NextDir, Cost) = open_queue.pop() #Popping the first entry of the OPEN
    closed_list.append(state)    #Adding the base node to the list of visited nodes

    while not problem.isGoalState(state) :  # Keep exploring if we haven't reached the goal state
        #print(state)
        next_nodes = problem.getSuccessors(state) # Getting the child nodes
        for node in next_nodes:
            n1 = node[0]    # Node
            d1 = node[1]    # Direction of node
            c1 = node[2]    # Cost of Node
            if ((problem.isGoalState(n1)) or (not n1 in closed_list)):
            #Checking if the node is the goal state or has been visited already
                open_queue.push((n1, NextDir + [d1], Cost + c1))
                closed_list.append(n1) #Adding the node to visited node lists
            #Pop the next node on the stack
        (state, NextDir, Cost) = open_queue.pop()
    return NextDir

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first"""
    "*** YOUR CODE HERE ***"
    # We'll use the PriorityQueue Datastructure from util.py to implement UCS
    # The cost function for UCS will be the total path length to that node.

    #This function will extract priority of each node in the Priority Queue
    # We will pass it as an argument when instantiating the PriorityQueueWithFunction Datastructure

    def path_cost(path_a):
        return problem.getCostOfActions([path[1] for path in path_a][1:])
    pri_queue = util.PriorityQueueWithFunction(path_cost)

    closed_list = []    # Keeping track of visited nodes
    start_state = problem.getStartState()   # Getting the start state of the Problem
    pri_queue.push([(start_state, [], 0)])

    while not pri_queue.isEmpty(): #Keep searching until OPEN is not empty (Differs from the previous implementation)
        search_p = pri_queue.pop()  #The path that we will consider for searching is popped from the PriorityQueue

        #We select the current node from the search path
        c_node = search_p[-1][0] # This will provide with the corrdinates of the last element in the search path

        #Now, we check if the current node is the goal state
        if problem.isGoalState(c_node):
            #if true, we return the directions for the pacman to follow
            final_path = [p[1] for p in search_p] #to remove the first entry from the result
            return final_path[1:]

        if c_node not in closed_list:
            for next_node in problem.getSuccessors(c_node): #this gives the successors of the current node
                if next_node[0] not in closed_list: #Checking whether it's been visited already
                    updated_path = search_p[:] #Copying all the tuples currently stored in the Search Path
                    updated_path.append(next_node)  #this updates the current path
                    pri_queue.push(updated_path)
            closed_list.append(c_node) #Updating closed list to indicate that current node has been visited
    return False    #Incase the search doesn't find goal state


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # A* Search differs from UCS on the fact that the total cost is a sum of the
    # backward path lenght and the distance to the goal. We are already using the
    # backward path length in UCS, and for this, we'll add the manhattanDistance
    # heuristic to the cost
    #function that calculates cost for PriorityQueue (F(n) = G(n) + H(n) )
    def total_cost(path_a):
        g = problem.getCostOfActions([path[1] for path in path_a][1:])
        h = heuristic(path_a[-1][0], problem)
        fn = g+h
        #h = manhattanHeuristic(path_a[-1][0], problem)
        #h = euclideanHeuristic(path_a[-1][0], problem)
        return (fn )

    pri_queue = util.PriorityQueueWithFunction(total_cost)

    closed_list = []    # Keeping track of visited nodes
    start_state = problem.getStartState()   # Getting the start state of the Problem
    pri_queue.push([(start_state, [], 0)])

    while not pri_queue.isEmpty(): #Keep searching until OPEN is not empty (Differs from the previous implementation)
        search_p = pri_queue.pop()  #The path that we will consider for searching is popped from the PriorityQueue

        #We select the current node from the search path
        c_node = search_p[-1][0] # This will provide with the corrdinates of the last element in the search path

        #Now, we check if the current node is the goal state
        if problem.isGoalState(c_node):
            #if true, we return the directions for the pacman to follow
            final_path = [p[1] for p in search_p] #to remove the first entry from the result
            return final_path[1:]

        if c_node not in closed_list:
            for next_node in problem.getSuccessors(c_node): #this gives the successors of the current node
                if next_node[0] not in closed_list: #Checking whether it's been visited already
                    updated_path = search_p[:] #Copying all the tuples currently stored in the Search Path
                    updated_path.append(next_node)  #this updates the current path
                    pri_queue.push(updated_path)
            closed_list.append(c_node) #Updating closed list to indicate that current node has been visited
    return False    #Incase the search doesn't find goal state



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
