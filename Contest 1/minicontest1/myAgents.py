# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'): # 'MyAgent' 'AStarFoodAgent' 'ClosestDotAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

pacmns =[]
food_lst =[]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"

        global pacmns   #declaring the global variables
        global food_lst
        index = self.index #index of the Agent
        #First four lines copied from ClosestDotAgent
        startPosition = state.getPacmanPosition(self.index)
        food = state.getFood()
        walls = state.getWalls()
        problem = AnyFoodSearchProblem(state, self.index)

        f_in_i, f_in_j = food_lst[index]
        f =0#Flag variable
        if (f_in_i, f_in_j) == (-1, -1) or food[f_in_i][f_in_j] is False or len(pacmns[index]) <2:
            #If food doesn't exist at the location, or this is the first iteration (Default values)
            for a in range(food.width):
                for b in range(food.height):
                    if food[a][b]: #food exists at the location
                        #path = search.astar(problem)
                        path = search.bfs(problem)
                        #path = search.ucs(problem)
                        pacmns[index] = path  # Add the path to the pacmns variable

                        food_lst[index] = (a, b) #Update the list to the food corner_coordinates
                        #print(food_lst)
                        #print(a,b)
                        #cost = len(path)
                        #print(cost)
                        x = 0
                        for i in range(len(food_lst)):
                            if food_lst[i] == [i,b]:
                                x +=1
                        f= (x<2)
                        if f:
                            break
                if f:
                    #print(food_lst)
                    break
        else:
            del(pacmns[index][0])
        #print("123")
        return pacmns[index][0]
        #raise NotImplementedError()

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
        #declaring the global variables

        global pacmns
        global food_lst #stores locations of the nearest food pallet for each agent
        pacmns = []
        food_lst = []
        for i in range(10):
            pacmns.append([1])
            food_lst.append([-1, -1])
#        raise NotImplementedError()

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""
class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"

        ## Code Added
        result = search.ucs(problem)
        return result
        #util.raiseNotDefined()

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]



### Added CODE
# class AStarFoodAgent(Agent):
#     "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
#     def __init__(self):
#         self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
#         self.searchType = FoodSearchProblem
#
# def foodHeuristic(state, problem):
#     """
#     Your heuristic for the FoodSearchProblem goes here.
#
#     This heuristic must be consistent to ensure correctness.  First, try to come
#     up with an admissible heuristic; almost all admissible heuristics will be
#     consistent as well.
#
#     If using A* ever finds a solution that is worse uniform cost search finds,
#     your heuristic is *not* consistent, and probably not admissible!  On the
#     other hand, inadmissible or inconsistent heuristics may find optimal
#     solutions, so be careful.
#
#     The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
#     (see game.py) of either True or False. You can call foodGrid.asList() to get
#     a list of food coordinates instead.
#
#     If you want access to info like walls, capsules, etc., you can query the
#     problem.  For example, problem.walls gives you a Grid of where the walls
#     are.
#
#     If you want to *store* information to be reused in other calls to the
#     heuristic, there is a dictionary called problem.heuristicInfo that you can
#     use. For example, if you only want to count the walls once and store that
#     value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
#     Subsequent calls to this heuristic can access
#     problem.heuristicInfo['wallCount']
#     """
#     position, foodGrid = state
#     "*** YOUR CODE HERE ***"
#
#     x,y = position
#     #print(foodGrid)
#     #print(position)
#     # foodgrid gives the coordinates of where the food is located,
#     f_list = foodGrid.asList()
#     #print(food_list)
#     #print(len(f_list))
#     f_dist = []
#     if (len(f_list)==0):
#         return 0
#     for xx, yy in f_list:
#         a = mazeDistance((x,y),(xx,yy), problem.startingGameState)
#         #Calculating the distance from our location to all the food locations
#         f_dist.append(a)
#     heuristic_x = max(f_dist) #Finding the path length to the farthest food point
#     #Nodes expanded for this: 4137
#     return heuristic_x

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        ## Code Added
        return self.food[x][y]
        #util.raiseNotDefined()
