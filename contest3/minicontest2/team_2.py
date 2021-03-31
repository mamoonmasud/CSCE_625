# myTeam.py
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
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
			   first = 'OffensiveReflexAgent', second = 'DefensiveAgent'):
	return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class AlphaBetaAgent(CaptureAgent):

	# Register initial state for AlphaBetaAgent include start position of the
	# agent, closest food position to the center and timer for defensive agent,
	# and mid point for center position.
	def registerInitialState(self, gameState):
		CaptureAgent.registerInitialState(self, gameState)
		self.start = gameState.getAgentPosition(self.index)
		self.closestFoodToCenter = None
		self.timer = 0
		self.opponent = self.getOpponents(gameState)

		# Setting up center position and check if the center position has a wall.
		midHeight = int(gameState.data.layout.height/2)
		midWidth = int(gameState.data.layout.width/2)
		while(gameState.hasWall(midWidth, midHeight)):
			midHeight -= 1
			if midHeight == 0:
				midHeight = gameState.data.layout.height
		self.midPoint = (midWidth, midHeight)
		
		print(self.midPoint)

		# Register team's agent.
		agentsTeam = []
		agentsLen = gameState.getNumAgents()
		i = self.index
		if self.red:
			print("we are red")
		while len(agentsTeam) < (agentsLen/2):
			agentsTeam.append(i)
			i += 2
			if i >= agentsLen:
				i = 0
		agentsTeam.sort()

		self.registerTeam(agentsTeam)




	def alphabeta(self, gameState, agent, mdepth, alpha, beta, visibleAgents):

		# restart the agent number if it passed the agents length
		if agent >= gameState.getNumAgents():
			agent = 0

		# add the depth if the alpha beta done a single loop
		if agent == self.index:
			mdepth += 1

		# pass the agent if it is not on the visible agents.
		if agent not in visibleAgents:
			return self.alphabeta(gameState, agent + 1, mdepth, alpha, beta, visibleAgents)

		# evaluate the gameState if the depth is 1 or the game is over and its the current agent.
		if mdepth == 1 or gameState.isOver():
			if agent == self.index:
				return self.evaluate(gameState)
			else:
				self.alphabeta(gameState, agent + 1, mdepth, alpha, beta, visibleAgents)

		legalActions = gameState.getLegalActions(agent)
		if agent in self.agentsOnTeam:
			v = float("-inf")
			for action in legalActions:
				v = max(v, self.alphabeta(gameState.generateSuccessor(agent, action), agent + 1,mdepth, alpha, beta, visibleAgents))
				if v >= beta:
					return v
				alpha = max(alpha, v)
			return v
		else:
			v = float("inf")
			for action in legalActions:
				v = min(v, self.alphabeta(gameState.generateSuccessor(agent, action), agent + 1,mdepth, alpha, beta, visibleAgents))
				if v <= alpha:
					return v
				beta = min(beta, v)
			return v


	def getSuccessor(self, gameState, action):
		"""
		Finds the next successor which is a grid position (location tuple).
		"""
		successor = gameState.generateSuccessor(self.index, action)
		pos = successor.getAgentState(self.index).getPosition()
		if pos != nearestPoint(pos):
		  # Only half a grid position was covered
			return successor.generateSuccessor(self.index, action)
		else:
			return successor

	def getFeatures(self, gameState):
		"""
		Returns a counter of features for the state
		"""
		features = util.Counter()
		features['successorScore'] = self.getScore(gameState)
		return features


	def getWeights(self, gameState):
		"""
		Normally, weights do not depend on the gamestate.  They can be either
		a counter or a dictionary.
		"""
		return {'successorScore': 1.0}


	def evaluate(self, gameState):
		"""
		Computes a linear combination of features and feature weights
		"""
		features = self.getFeatures(gameState)
		weights = self.getWeights(gameState)
		return features * weights

class OffensiveAgent(AlphaBetaAgent):
	# The basic of offensive agent is to grab all the food while avoiding ghost.
	

	def chooseAction(self, gameState):
		start = time.time()

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() is not None]
		#print(visibleAgents)
		# Start alpha beta pruning algorithm
		v = (float("-inf"), 'None')
		alpha = float('-inf')
		beta = float('inf')
		legalActions = gameState.getLegalActions(self.index)
		legalActions.remove(Directions.STOP)

		act_x = None
		print(legalActions)

		if(len(legalActions)!=0):
		# 	return(legalActions)
		# else:

			for action in legalActions:
				v = max(v, (self.alphabeta(gameState.generateSuccessor(self.index, action), self.index+1, 0, alpha, beta, visibleAgents), action))
				#print(v)
				if v[0] > beta:
					print("Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0]))
					#print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)
					print("Trump")
					return v[1]
				alpha = max(alpha, v[0])

			prob = util.flipCoin(0.1)
			
			if prob:
				act_x = random.choice(legalActions)
			else:
				act_x = v[1]				

		#print("aa Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0]))
		#print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)
		print(act_x)
		return act_x

	
	def getFeatures(self, gameState):
		features = util.Counter()
		foodList = self.getFood(gameState).asList()
		# Check if agent is red or blue. red team will want a higher score
		# while blue team want a lower score
		if self.red:
			features['successorScore'] = gameState.getScore()

		else:
			features['successorScore'] = -1* gameState.getScore()
		features['successorScore'] -= len(foodList)
		
		features['distanceToGhost'] = 0

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() != None]

		if not set(visibleAgents).isdisjoint(self.getOpponents(gameState)):
			
			# Agent will need to distance themself from ghost if agent is a pacman or agent is scared.
			if gameState.getAgentState(self.index).isPacman and gameState.getAgentState(self.index).scaredTimer > 0:
				print("RUN")
				ghosts = list(set(visibleAgents).intersection(self.getOpponents(gameState)))
				for ghost in ghosts:
					ghostPos = gameState.getAgentState(ghost).getPosition()
					dist = self.getMazeDistance(currPos, ghostPos)
					# Agent will never move to less than 2 distance.
					if dist <= 2:
						print("This runs")
						features['distanceToGhost'] = -9999
					else:
						features['distanceToGhost'] += 0.5 * dist
						print("Trump")
			# Agent does not need to further itself from the ghost but it is better to avoid/hide from it.
			# else:
			# 	#print("ahole")
			# 	ghosts = (set(visibleAgents).intersection(self.getOpponents(gameState)))
			# 	for ghost in ghosts:
			# 		ghostPos = gameState.getAgentState(ghost).getPosition()

			# 		dist = self.getMazeDistance(currPos, ghostPos)
			# 		print("distance to ghost ", dist)

			# 		features['distanceToGhost'] += 0.5 * dist
		# If no opponent are visible, agent will just try to read the noise distance and try to
		# stay away from it.
		else:
			print("Hello")
			ghosts = list(set(allAgents).difference(self.agentsOnTeam))
			for ghost in ghosts:
				ghostDists = gameState.getAgentDistances()
				features['distanceToGhost'] += ghostDists[ghost]


		# Agent will grab the nearest food unless it's already carrying more than 5 food.
		if gameState.getAgentState(self.index).numCarrying < 5:
			myPos = gameState.getAgentState(self.index).getPosition()
			
			if len(foodList) > 0:
				minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
				features['distanceToFood'] = minDistance
				#print(minDistance)

			else:
				myPos = gameState.getAgentState(self.index).getPosition()
				features['distanceToFood'] = self.getMazeDistance(myPos, self.start)
		else:
			myPos = gameState.getAgentState(self.index).getPosition()
			features['distanceToFood'] = self.getMazeDistance(myPos, self.start)

		return features

	def getWeights(self, gameState):
		return {'successorScore': 100, 'distanceToFood': -1, 'distanceToGhost': 1}

class DefensiveAgent(AlphaBetaAgent):
	# The basic of defensive agent is to go around the nearest food to the center to detect an enemy
	# and chase one if found.
	def chooseAction(self, gameState):
		start = time.time()

		# Get all visible agents
		allAgents = range(0, gameState.getNumAgents())
		visibleAgents = [a for a in allAgents if gameState.getAgentState(a).getPosition() is not None]

		# Start alpha beta algorithm
		v = (float("-inf"), 'None')
		alpha = float('-inf')
		beta = float('inf')
		legalActions = gameState.getLegalActions(self.index)
		for action in legalActions:
			if action == 'Stop':
				continue
			v = max(v, (self.alphabeta(gameState.generateSuccessor(self.index, action), self.index+1, 0, alpha, beta, visibleAgents), action))
			if v[0] > beta:
				# print "Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0])
				# print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)
				return v[1]
			alpha = max(alpha, v[0])
		# print "Agent {0} chose {1} with value {2}".format(self.index, v[1], v[0])
		# print 'Execution time for agent %d: %.4f' % (self.index, time.time() - start)

		# Minus the timer for the patrol function.
		self.timer -= 1

		return v[1]

	def getFeatures(self, gameState):
		features = util.Counter()
		myState = gameState.getAgentState(self.index)
		myPos = myState.getPosition()
		foodList = self.getFoodYouAreDefending(gameState).asList()

		# Computes distance to invaders we can see
		enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
		invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
		features['numInvaders'] = len(invaders)

		# Check if any opponent is found.
		if len(invaders) > 0:
			dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
			features['invaderDistance'] = max(dists)
		else:
			# If no opponent is found, patrol around the 3 nearest food to the center.
			# if the nearest food to center is set, calculate the distance.
			if self.closestFoodToCenter:
				dist = self.getMazeDistance(myPos, self.closestFoodToCenter)
			else:
				dist = None

			# Recalculate the 3 nearest food when it's already 20 actions or the food
			# is reached.
			if self.timer == 0 or dist == 0:
				self.timer = 20
				foods = []
				for food in foodList:
					foods.append((self.getMazeDistance(self.midPoint, food), food))
				foods.sort()
				chosenFood = random.choice(foods[:3])
				self.closestFoodToCenter = chosenFood[1]
			dist = self.getMazeDistance(myPos, self.closestFoodToCenter)
			features['invaderDistance'] = dist
		return features

	def getWeights(self, gameState):
		return {'numInvaders': -1000, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}


	def getBestAction(self, gameState, targetPos, actions):
		minDis, bestAction = min([(self.getMazeDistance(self.getSuccessor(gameState, action), targetPos), action) for action in actions]) 
		#print("best action", minDis, action)
		#print([(self.getMazeDistance(self.getSuccessor(gameState, action), targetPos), action) for action in actions])
		return (minDis, bestAction)

	def getBestActionAvoidOneGhost(self, gameState, opponentPos, actions):
		maxDis, bestAction = max([(self.simulateAvoidOneGhost(gameState.generateSuccessor(self.index, action), 3, opponentPos), action) for action in actions]) 
		return bestAction

	def getBestActionAvoidTwoGhosts(self, gameState, opponent1Pos, opponent2Pos, actions):
		maxDis, bestAction = max([(self.simulateAvoidTwoGhosts(gameState.generateSuccessor(self.index, action), 3, opponent1Pos, opponent2Pos), action) for action in actions]) 
		return bestAction


class OffensiveReflexAgent(CaptureAgent):
	
	def registerInitialState(self, gameState):
		"""
		This method handles the initial setup of the
		agent to populate useful fields (such as what team
		we're on).
		A distanceCalculator instance caches the maze distances
		between each pair of positions, so your agents can use:
		self.distancer.getDistance(p1, p2)
		IMPORTANT: This method may run for at most 15 seconds.
		"""

		'''
		Make sure you do not delete the following line. If you would like to
		use Manhattan distances instead of maze distances in order to save
		on initialization time, please take a look at
		CaptureAgent.registerInitialState in captureAgents.py.
		'''

		CaptureAgent.registerInitialState(self, gameState)

		'''
		Your initialization code goes here, if you need any.
		'''
		#self.start = gameState.getAgentPosition(self.index)

		if self.red:
			centralX = int((gameState.data.layout.width - 2) / 2)
		else:
			centralX = int((gameState.data.layout.width - 2) / 2) + 1
		self.boundary = []
		
		for i in range(1, gameState.data.layout.height - 1):
			if not gameState.hasWall(centralX, i):
				self.boundary.append((centralX, i))
		self.nearestFood = self.getFurthestTarget(gameState, gameState.getAgentState(self.index).getPosition(), self.getFood(gameState).asList())
		self.team = self.getTeam(gameState)
		self.opponent = self.getOpponents(gameState)
		self.randFoodStatus = 0
		self.randFood = random.choice(self.getFoodYouAreDefending(gameState).asList())
		if self.index == self.team[0]: 
			self.partnerIndex = self.team[1]
		else: 
			self.partnerIndex = self.team[0]



				

	def getNearestTarget(self, gameState, pos, targets):
		minDis, nearestTarget = min([(self.getMazeDistance(pos, target), target) for target in targets])
		return (minDis, nearestTarget)
	
	
	def getFurthestTarget(self, gameState, pos, targets):
		maxDisttoTarget, furthestTarget = max([(self.getMazeDistance(pos, target), target) for target in targets])
		return furthestTarget

	def getSuccessor(self, gameState, action):
		"""
		Finds the next successor which is a grid position (location tuple).
		"""
		successor = gameState.generateSuccessor(self.index, action)
		pos = successor.getAgentState(self.index).getPosition()
		if pos != nearestPoint(pos):
			# Only half a grid position was covered
			return successor.generateSuccessor(self.index, action)
		else:
			return pos

	def getBestAction(self, gameState, targetPos, actions):
		minDis, bestAction = min([(self.getMazeDistance(self.getSuccessor(gameState, action), targetPos), action) for action in actions]) 
		#print("best action", minDis, action)
		#print([(self.getMazeDistance(self.getSuccessor(gameState, action), targetPos), action) for action in actions])
		return (minDis, bestAction)

	def getBestActionAvoidOneGhost(self, gameState, opponentPos, actions):
		maxDis, bestAction = max([(self.simulateAvoidOneGhost(gameState.generateSuccessor(self.index, action), 3, opponentPos), action) for action in actions]) 
		return bestAction
	
	def getBestActionAvoidTwoGhosts(self, gameState, opponent1Pos, opponent2Pos, actions):
		maxDis, bestAction = max([(self.simulateAvoidTwoGhosts(gameState.generateSuccessor(self.index, action), 3, opponent1Pos, opponent2Pos), action) for action in actions]) 
		return bestAction

	def isAtDoor(self, gameState):
		myPos = gameState.getAgentState(self.index).getPosition()
		if myPos in self.boundary: 
			return True
		else: 
			return False
			
	def simulateAvoidOneGhost(self, gameState, depth, opponentPos):
		#print("working1")
		state = gameState.deepCopy()
		
		if depth == 0:
			return self.getMazeDistance(state.getAgentPosition(self.index), opponentPos)
		else: 
			actions = state.getLegalActions(self.index)
			disToGhost = [self.simulateAvoidOneGhost(state.generateSuccessor(self.index, action), depth - 1, opponentPos) for action in actions]
			return sum(disToGhost)/len(disToGhost)

	def simulateAvoidTwoGhosts(self, gameState, depth, opponent1Pos, opponent2Pos):
		#print("working2")
		state = gameState.deepCopy()
	
		if depth == 0:
			return self.getMazeDistance(state.getAgentPosition(self.index), opponent1Pos) + self.getMazeDistance(state.getAgentPosition(self.index), opponent2Pos)
		else: 
			actions = state.getLegalActions(self.index)
			disToGhost = [self.simulateAvoidTwoGhosts(state.generateSuccessor(self.index, action), depth - 1, opponent1Pos, opponent2Pos) for action in actions]
			return sum(disToGhost)/len(disToGhost)