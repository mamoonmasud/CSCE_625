# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, sys

from game import Agent

def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        """
        Sample Output of successorGameState

        %%%%%%%%%%%%%%%%%%%%
        %o...%        %....%
        %.%%G% %%%%%% %.%%.%
        %.%.. <...... ...%.%
        %.%.%%.%%  %% %%.%.%
        %......%    % G....%
        %.%.%%.%%%%%% %%.%.%
        %.%.......... ...%.%
        %.%%.%.%%%%%% %.%%.%
        %....%...     %...o%
        %%%%%%%%%%%%%%%%%%%%
        Score: 197
        < is the Pacman.
        % are walls
        G is the ghost
        ... is the food.
        o is the power pallet


        newPos gives out a tuple for the next position of the PacMan:e.g (12, 3)

        newFood gives out locations of the food pallets: e.g
        FFFFFFFFFFFFFFFFFFFF
        FFTTTFTTTTTTTTFTTTTF
        FTFFTFTFFFFFFTFTFFTF
        FTFTTTTTTTTTTTTTTFTF
        FTFTFFTFFFFFFTFFTFTF
        FTTTTTTFFFFFFTTTTTTF
        FTFTFFTFFFFFFTFFTFTF
        FTFTTTTTTTTTTTTTTFTF
        FTFFTFTFFFFFFTFTFFTF
        FTTTTFTTFFTTTTFTTTFF
        FFFFFFFFFFFFFFFFFFFF

        newScaredTimes gives out the time remaining for which the Ghosts will
        remain scared. If one is eaten, the time for that ghost is reset to 0.
        The max time is 40 secs (at the beginning)

        getGhostState (1/2) gives the position and direction of the Ghost indexed
        Ghost: (x,y)=(9.0, 6.0), North

        getGhostPosition(1) just gives out Ghost coordinates

        getCapsules() returns the coordinates of the remaining power pellets.
        [(18, 1), (1, 9)]
        """
        "*** YOUR CODE HERE ***"
        # print(successorGameState)
        # print(newPos)
        # print(newScaredTimes)
        # print(successorGameState.getCapsules())
        #
        # We need to convert the food points from a Grid of type Boolean to
        # coordinates array, so we are able to use it in the evaluation function.
        # Python's as list function does this.

        new_food_grid = newFood.asList()

        # Now we calculate the Manhattan Distance from the Pacman's Location to
        # all the food points that are still available and sort them out in
        # ascending order.
        food_distances = []
        min_food_distance = 100
        for food_Positions in new_food_grid:
            min_food_distance = min(100, manhattanDistance(newPos, food_Positions))
        # food_distances.sort()
        # if food_distances[0]:
        #     min_food_distance = food_distances[0]
        # else:
        #     min_food_distance = 100

        # min_food_distance  =min(100, (food_dist for food_dist in food_distances))
        # print(min_food_distance)

        # Now that we have figured out the distance of food pallets from PacMan,
        # we will calculate the distance of PacMan from the Ghosts
        ghosts_man_dist = []
        for ghostState in newGhostStates:
            ghosts_man_dist.append(manhattanDistance(newPos, ghostState.getPosition()))
        #ghosts_man_dist.sort()
        #print(ghosts_man_dist) #Gives the Manhattan distance of the Pacman to the Ghosts
        min_ghost_dist = min(ghosts_man_dist)
        min_index = ghosts_man_dist.index(min_ghost_dist)
        #Gives out the index of the Ghost with minimum Manhattan Distance
        #print(min_index)
        #print(successorGameState.getNumFood()) #gives the remaining foodpallets

        if ghosts_man_dist[min_index] <3:
            if newScaredTimes[min_index] <2:
                return -float('inf')

        game_score = successorGameState.getScore()
        # if food_distances:
        #         food_dist_inv = 1/food_distances[0]
                #print(food_dist_inv)
                #e_score+= (game_score +food_distances[0])
                #print(successorGameState.getScore() + ((1 / min_food_distance)))
                # return game_score + ((1 /min_food_distance))
        return game_score + (1 /min_food_distance)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


## Minimax Agent for adversarial search

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #a = gameState.getLegalActions(0)
        #Returns the legal actions PacMan can from the current position.
        # e.g. ['West', 'Stop', 'East', 'North']
        #print(a)
        # print(gameState.isWin())
        # print(gameState.isLose())
        #print(self.evaluationFunction(gameState))

        return self.max_value(gameState, 0, 0)[1]


    def mini_max_algo(self, gameState, agent_index, depth):    #Calculates the minimax value
        if gameState.isWin() or gameState.isLose(): #If the Game State is a win or
        # Lose Game State(terminal state), we will return the state's utility.
            return self.evaluationFunction(gameState)
        else:
            #Updating the agent_index if the next state is not terminal
            next_agent_index = (agent_index + 1) % gameState.getNumAgents() #Making sure that the agent index remains between 0 and no.of agents -1
            #Checking if the next state is a Max State or Min State.
            #print(self.depth)
            if next_agent_index ==0: #If it's a max State, we'll return the max value
                if depth >= self.depth-1:
                    return self.evaluationFunction(gameState)
                return self.max_value(gameState, next_agent_index, depth + 1)[0]
            else:   #if it's a min state, we'll get the min value and return it
                return self.min_value(gameState, next_agent_index, depth)[0]


    def max_value(self, gameState, agent_index, depth):
        max_v = (float("-inf"), None)   #initializing max_v to -infinity.
        #First we get the Actions that the PacMan can do at the position from legalaction method
        actions = gameState.getLegalActions(agent_index)
        for action in actions:  #For all the successors/legal actions of the current state, we'll get the max.
            new_v = self.mini_max_algo(gameState.generateSuccessor(agent_index, action), agent_index, depth)

            if new_v > max_v[0]: #if the action is greater than the previously
                                 # saved in max_v, we'll update the value of max_v
                max_v = (new_v, action)
        return max_v

    def min_value(self, gameState, agent_index, depth):

        min_v = (float("inf"), None) #initializing min_v to +infinity.
        actions = gameState.getLegalActions(agent_index)    #Getting the legal actions
        for action in actions: #For all the successors/legal actions of the current state, we'll get the minimum valued one.
            new_v = self.mini_max_algo(gameState.generateSuccessor(agent_index, action), agent_index, depth)
            if new_v < min_v[0]:    # if the new value is less than already saved one, we'll update the min value to the new one
                min_v = (new_v, action)
        return min_v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # The challenge is to generalize the Agent
        return self.max_value(gameState, (float("-inf"),None), (float("inf"), None), 0, 0)[1]



    def min_max_alpha_beta(self, gameState, alpha, beta, agent_index, depth):    #Calculates the minimax value
        if gameState.isWin() or gameState.isLose(): #If the Game State is a win or
        # Lose Game State(terminal state), we will return the state's utility.
            return self.evaluationFunction(gameState)
        else:
            #Updating the agent_index if the next state is not terminal
            next_agent_index = (agent_index + 1) % gameState.getNumAgents() #Making sure that the agent index remains between 0 and no.of agents -1
            #Checking if the next state is a Max State or Min State.
            #print(self.depth)
            if next_agent_index ==0: #If it's a max State, we'll return the max value
                if depth >= self.depth-1:
                    return self.evaluationFunction(gameState)
                return self.max_value(gameState, alpha, beta, next_agent_index, depth + 1)[0]
            else:   #if it's a min state, we'll get the min value and return it
                return self.min_value(gameState, alpha, beta, next_agent_index, depth)[0]

    # Following the given pseudo-codes, we'll update the maximum value
    # and minimum value functions.

    def max_value(self, gameState, alpha, beta, agent_index, depth):
        max_v = (float("-inf"), None)   #initializing max_v to -infinity.
        #First we get the Actions that the PacMan can do at the position from legalaction method
        actions = gameState.getLegalActions(agent_index)
        for action in actions:  #For all the successors/legal actions of the current state, we'll get the max.
            new_v = self.min_max_alpha_beta(gameState.generateSuccessor(agent_index, action),alpha, beta, agent_index, depth)
            if new_v > max_v[0]: #if the action is greater than the previously
                                 # saved in max_v, we'll update the value of max_v
                max_v = (new_v, action)
            if max_v[0]> beta[0]:  #If the current maximum value is greater than beta, we return the value
            # You must not prune on equality in order to match the set of states explored by our autograder
            # Therefore, we don't prone on equality.
                return max_v
            if max_v[0] > alpha[0]: #Update the value of alpha if max_v is greater than current value of alpha
                alpha = max_v
        return max_v

    def min_value(self, gameState, alpha, beta, agent_index, depth):
        min_v = (float("inf"), None) #initializing min_v to +infinity.
        actions = gameState.getLegalActions(agent_index)    #Getting the legal actions
        for action in actions: #For all the successors/legal actions of the current state, we'll get the minimum valued one.
            new_v = self.min_max_alpha_beta(gameState.generateSuccessor(agent_index, action),alpha, beta, agent_index, depth)
            if new_v < min_v[0]:    # if the new value is less than already saved one, we'll update the min value to the new one
                min_v = (new_v, action)
            if min_v[0] < alpha[0]: #If the current minimum value is less than alpha, we return the value
                return min_v
            if min_v[0] < beta[0]:  #Update the value of beta if min_v is greater than current value of beta
                beta = min_v
        return min_v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, 0, 0)[1]

    def expectimax_algo(self, gameState, agent_index, depth):    #Calculates the minimax value
        if gameState.isWin() or gameState.isLose(): #If the Game State is a win or
        # Lose Game State(terminal state), we will return the state's utility.
            return self.evaluationFunction(gameState)
        else:
            #Updating the agent_index if the next state is not terminal
            next_agent_index = (agent_index + 1) % gameState.getNumAgents() #Making sure that the agent index remains between 0 and no.of agents -1
            #Checking if the next state is a Max State or Min State.
            #print(self.depth)
            if next_agent_index ==0: #If it's a max State, we'll return the max value
                if depth >= self.depth-1:
                    return self.evaluationFunction(gameState)
                return self.max_value(gameState, next_agent_index, depth + 1)[0]
            else:   #if it's a min state, we'll get the min value and return it
                return self.min_value(gameState, next_agent_index, depth)[0]


    def max_value(self, gameState, agent_index, depth): #This is the same as Minimax, because we only model the adversary as probabilitic function.
        max_v = (float("-inf"), None)   #initializing max_v to -infinity.
        #First we get the Actions that the PacMan can do at the position from legalaction method
        actions = gameState.getLegalActions(agent_index)
        for action in actions:  #For all the successors/legal actions of the current state, we'll get the max.
            new_v = self.expectimax_algo(gameState.generateSuccessor(agent_index, action), agent_index, depth)

            if new_v > max_v[0]: #if the action is greater than the previously
                                 # saved in max_v, we'll update the value of max_v
                max_v = (new_v, action)
        return max_v

    def min_value(self, gameState, agent_index, depth):

        exp_v = (0, None) #initializing min_v to
        actions = gameState.getLegalActions(agent_index)    #Getting the legal actions (as it's given that we can consider just the legal actions)
        for action in actions: #For all the successors/legal actions of the current state, we'll get the minimum valued one.
            min_value = self.expectimax_algo(gameState.generateSuccessor(agent_index, action), agent_index, depth)
            prob = (1/len(actions))*min_value #Calculating the probability of the successor
            exp_v = (prob + exp_v[0], 0)
        return exp_v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    " The below code is copied from the evaluation function written earlier for Reflex Agent"
    "It just focuses on getting data from game state."


    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    new_food_grid = newFood.asList()
    newGhostStates = currentGameState.getGhostStates()
    newGhostPositions = currentGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    food_remaining = currentGameState.getNumFood()
    pellets_remaining = len(currentGameState.getCapsules())

    # Now we calculate the Manhattan Distance from the Pacman's Location to
    # all the food points that are still available and sort them out in
    # ascending order.
    #food_distances = []
    min_food_distance = 100
    for food_Positions in new_food_grid:
        min_food_distance = min(min_food_distance, manhattanDistance(newPos, food_Positions))

    # Now that we have figured out the distance of food pallets from PacMan,
    # we will calculate the distance of PacMan from the Ghosts
    ghosts_man_dist = []
    dist_ghost = 0
    for ghostState in newGhostPositions:
        dist_ghost = manhattanDistance(newPos, ghostState)
        ghosts_man_dist.append(dist_ghost)
        if (dist_ghost <2):
            return -float('inf')
        #print(manhattanDistance(newPos, ghostState))
    #ghosts_man_dist.sort()
    #print(ghosts_man_dist) #Gives the Manhattan distance of the Pacman to the Ghosts


    min_ghost_dist = min(ghosts_man_dist)
    min_index = ghosts_man_dist.index(min_ghost_dist)


    #Gives out the index of the Ghost with minimum Manhattan Distance
    #print(min_index)
    #print(successorGameState.getNumFood()) #gives the remaining foodpallets
    # ghosts_man_dist = 0
    # for ghostState in newGhostPositions:
    #     ghosts_man_dist = manhattanDistance(newPos, ghostState)
    misc_weight = 0
    #Penalizing loosing states and giving benefit for winning states
    if currentGameState.isLose():
        misc_weight -= 500
    elif currentGameState.isWin():
        misc_weight += 500
    #ghosts_man_dist[min_index] + \
    #Defining weights for remaining food, remaining pellets, and the distance of the nearest food
    remaining_food_weight  = 1000000
    remaining_pellets_weight  = 10000
    closest_food_weight  = 1000
    """
    Final value of the evaluation function depends on the weighted closest 
    food distance, weighted food remaining, weighted pellets remaining, distance
    to the closest ghost, and whether the state is winning or losing state.
    """
    final_weighted_value = 1.0/(min_food_distance+1)*closest_food_weight + 1.0/(food_remaining +1) *remaining_food_weight \
                              + 1.0/(pellets_remaining+1) * remaining_pellets_weight + ghosts_man_dist[min_index]+ misc_weight
    return final_weighted_value
# # Abbreviation
better = betterEvaluationFunction
