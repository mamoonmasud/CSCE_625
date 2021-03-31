# team_1.py
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

from util import nearestPoint, normalize, manhattanDistance

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'Attack_Agent', second = 'Defen_Agent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class alphabeta_agent (CaptureAgent):
  '''
  Registering the initial state for Alpha Beta Agent
  Including Start Position, closest food position & 
  Timer for the defensive agent
  '''
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    self.start = gameState.getAgentPosition(self.index)
    self.timer = 0
    self.closestFoodtoCenter= None #For storing closest food position

    # Finding center position, and checking if it has a wall
    cen_y = int(gameState.data.layout.height/2)
    cen_x = int(gameState.data.layout.width/2)
    #checking if there's a wall at the center position
    while(gameState.hasWall(cen_x, cen_y)):
      cen_y -=1

      if cen_y ==0:
        cen_y = gameState.data.layout.height
    
    # Saving the midpoint coordinates. (midpoint where the wall doesn't exist)
    self.midPoint = (cen_x, cen_y)

    #registering agent
    agents_team =[]

    agents_len = gameState.getNumAgents()

    i = self.index
    while len(agents_team) < (agents_len/2):
      agents_team.append(i)
      i+=2
      if i >= agents_len:
        i =0

    agents_team.sort()

    self.registerTeam(agents_team)


### The below is implementation of Alpha Beta Algorithm (Minimax with alpha-beta pruning)

  def alphabeta (self, gameState, agent, dep, alpha, beta, vis_agent):


    if agent >=gameState.getNumAgents():
      agent =0 #We reset the agent number after iterating over all the agents

    if agent ==self.index:
      dep+=1

    if agent not in vis_agent:

      return self.alphabeta(gameState, agent+1, dep, alpha, beta, vis_agent)

    # Checking if Game is over, or depth is 1, and if the agent is the current agent,
    # we'll evaluate the gameState

    if gameState.isOver() or dep ==1:
      if agent == self.index:
        return self.evaluate(gameState)

      else:
        self.alphabeta(gameState, agent+1, dep, alpha, beta, vis_agent)

      leg_actions = gameState.getLegalActions(agent)

      #Checking if the agent is on our team
      
      if agent in self.agentsOnTeam:
        v = float("-inf")

        for action in leg_actions:
          v = max( v, self.alphabeta(gameState.generateSuccessor(agent, action), agent+1, dep, alpha, beta, vis_agent))

          if v > beta:
            return v
          alpha = max(alpha, v)
        return v

      else:
        v = float("inf")
        for action in leg_actions:
          v = min( v, self.alphabeta(gameState.generateSuccessor(agent, action), agent+1, dep, alpha, beta, vis_agent))

          if v < alpha:
            return v
          beta = min(beta, v)

        return v

  def it_dep (self, gameState, action, visibleAgents):

    successor = gameState.generateSuccessor(self.index, action)

    dep = 0

    with dep <5:
      leg_actions = successor.getLegalActions(self.index)

      illeg_actions = [actions, 'Stop']

      valid_actions = list(set(leg_actions).difference(set(illeg_actions)))

      if len(valid_actions)==0: # No Action other than STOP
        return 0
      if len(valid_actions) >1: # Not a dead-end
        return 1

      successor = gameState.generateSuccessor(self.index, action)

      dep+= 1

    if set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
      return 1
    else:
      return 0

  def fetch_features (self, gameState):
    #Feature counter is returned

    feat = util.Counter()
    feat['successorScore'] = self.getScore(gameState)

    return feat

  def fetch_weights(self, gameState):

    return {'successorScore':1.0}

  def evaluate(self, gameState):
    feat = self.fetch_features(gameState)
    weights = self.fetch_weights(gameState)

    return feat*weights


class Defen_Agent(alphabeta_agent):
  # This agent will be the defensive agent, and the basic task will be to 
  # detect an enemy and chase it if found

  def chooseAction(self, gameState):

    start = time.time()
    
    agent_list = range( 0, gameState.getNumAgents())
    visibleAgents = [agents for agents in agent_list if gameState.getAgentState(agents).getPosition() is not None]


    #Alpha Beta algo starts

    act_a = (float("-inf"), 'None')

    alpha = float('-inf')
    beta = float('inf')

    leg_actions = gameState.getLegalActions(self.index)

    for action in leg_actions:
      if action == 'Stop':
        continue
      act_a = max(act_a, (self.alphabeta(gameState.generateSuccessor(self.index, action), self.index+1, 0, alpha, beta, visibleAgents), action))

      if act_a[0] > beta:
        print("Agent{0} chose the action {1} having value {2}".format(self.index, act_a[1], act_a[0]))
        return act_a[1]

      alpha =max(alpha, act_a[0])
    self.timer -=1
    return act_a[1]
    

  def fetch_features(self, gameState):

    feat = util.Counter()

    my_state = gameState.getAgentState(self.index)
    
    my_pos = my_state.getPosition()

    #Getting the Opponents food (that we are to defend)
    opp_food = self.getFoodYouAreDefending(gameState).asList() 

    # Calculating the distance to the visible opponent

    enemy_x = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    enemy_y = [x for x in enemy_x if x.isPacman and x.getPosition() != None]
    
    feat['numInvaders'] = len(enemy_y)

    # checking if there's any enemy found
    if len(enemy_y) > 0:
      dists = [self.getMazeDistance(my_pos, a.getPosition()) for a in enemy_y]
      feat['invaderDistance'] = max(dists)

    else:
      # In case we find no visible enemy, we then find the nearest food 
      # in the center, and calculate distance to it. 

      if self.closestFoodToCenter:
        dist = self.getMazeDistance(my_pos, self.closestFoodToCenter)
      
      else:
        dist = None

      # We will check again for the nearest food pallet to the center, and
      # recalculate the distance if 15 actions are passed

      if self.timer == 0 or dist == 0:
        self.timer = 15


        enem_food = []

        for f in opp_food:

          enem_food.append((self.getMazeDistance(self.midPoint, f), f))

        enem_food.sort()
        #selecting 3 Food Pellets
        chosenFood = random.choice(enem_food[:3])

        self.closestFoodToCenter = chosenFood[1]

      dist_to_enemy_food = self.getMazeDistance(my_pos, self.closestFoodToCenter)
      feat['invaderDistance'] = dist_to_enemy_food
    return feat


  def fetch_weights(self, gameState):
    return {'numInvaders': -100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}



class Attack_Agent(alphabeta_agent):
  #This agent grabs food and avoids the ghost

  def chooseAction(self, gameState):

    start = time.time()
    
    agent_list = range( 0, gameState.getNumAgents())
    visibleAgents = [agents for agents in agent_list if gameState.getAgentState(agents).getPosition() is not None]

    #Alpha Beta pruning algo starts

    act_a = (float("-inf"), 'None')

    alpha = float('-inf')
    beta = float('inf')

    leg_actions = gameState.getLegalActions(self.index)

    for action in leg_actions:
      if action == 'Stop':
        continue
      sab = self.alphabeta(gameState.generateSuccessor(self.index, action), self.index+1, 0, alpha, beta, visibleAgents)
      print(sab)

      act_a = max(act_a, sab)

      if act_a[0] > beta:
        print("Agent{0} chose the action {1} having value {2}".format(self.index, act_a[1], act_a[0]))
        return act_a[1]

      alpha =max(alpha, act_a[0])
    return act_a[1]



  def fetch_features(self, gameState):

    feat = util.Counter()
    feat['ghost_dist'] =0

    #Getting the Opponents food (that we are to defend)
    food_list = self.getFood(gameState).asList() 

    #Checking if the agent is of red team or blue team
    if self.red:
      feat['successorScore'] = gameState.getScore()

    else:
      feat['successorScore'] = -1*gameState.getScore()

    feat['successorScore'] -= len(food_list)

    all_agents = range(0, gameState.getNumAgents())
    visibleAgents = [agents for agents in all_agents if gameState.getAgentState(agents).getPosition() is not None]

    pos_x = gameState.getAgentState(self.index).getPosition()

    if not set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
      # This checks if an opponent is among visible agents
      # Checking if the current agent is PACMAN, or a scared ghost

      if gameState.getAgentState(self.index).isPacman and gameState.getAgentState(self.index).scaredTimer > 0:
        
        ghost_list = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
        
        for ghost in ghost_list:
          ghostPos = gameState.getAgentState(ghost).getPosition()
        
          dist = self.getMazeDistance(pos_x, ghostPos)

          # distance can't be <= 2
          if dist <= 2:
            feat['ghost_dist'] = -9999

          else:
            feat['ghost_dist'] += 0.5 * dist

      # For the case when we don't have to move away from ghost
      else:
        ghost_list = list(set(visibleAgents).intersection(self.getOpponents(gameState)))

        for ghost in ghost_list:
          ghostPos = gameState.getAgentState(ghost).getPosition()
          dist = self.getMazeDistance(pos_x, ghostPos)

          # print "distance to ghost ", dist
          feat['ghost_dist'] += 0.5 * dist

    # The case when there's no ghost in visible agents, agent will read noise distance 

    else:
      ghost_list = list(set(allAgents).difference(self.agentsOnTeam))
      for ghost in ghost_list:
        ghostDists = gameState.getAgentDistances()
        feat['ghost_dist'] += ghostDists[ghost]

    # PACMAN will go to the nearest food pallet, if it's not already carrying 5 pallets
    
    if gameState.getAgentState(self.index).numCarrying < 5:
      agent_pos = gameState.getAgentState(self.index).getPosition()

      if len(food_list) > 0:
        #Finding the closest food pallet

        min_pallet_dist = min([self.getMazeDistance(agent_pos, food) for food in food_list])
        feat['food_dist'] = min_pallet_dist
      
      else: 
      #If foodlist is empty, PACMAN will go back
        agent_pos = gameState.getAgentState(self.index).getPosition()
        feat['food_dist'] = self.getMazeDistance(agent_pos, self.start)
    else:
      # If PACMAN already has 5 pallets, it will go back
      agent_pos = gameState.getAgentState(self.index).getPosition()
      feat['food_dist'] = self.getMazeDistance(agent_pos, self.start)
    return feat

  def getWeights(self, gameState):
    return {'successorScore': 100, 'food_dist': -1, 'ghost_dist': 1}
