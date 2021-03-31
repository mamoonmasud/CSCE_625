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
			   first = 'Defen_Agent', second = 'Offensive_Agent'):
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
		self.closestFoodToCenter= None #For storing closest food position

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



	def getFeatures (self, gameState):
	#Feature counter is returned

		feat = util.Counter()
		feat['successorScore'] = self.getScore(gameState)

		return feat

	def getWeights(self, gameState):

		return {'successorScore':1.0}

	def evaluate(self, gameState):
		feat = self.getFeatures(gameState)
		weights = self.getWeights(gameState)

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
		leg_actions.remove(Directions.STOP)
		for action in leg_actions:

			act_a = max(act_a, (self.alphabeta(gameState.generateSuccessor(self.index, action), self.index+1, 0, alpha, beta, visibleAgents), action))

			if act_a[0] > beta:
				return act_a[1]
			alpha =max(alpha, act_a[0])
		self.timer -=1
		return act_a[1]
		

	def getFeatures(self, gameState):

		feat = util.Counter()
		my_state = gameState.getAgentState(self.index)
		my_pos = my_state.getPosition()

		#Getting the Opponents food (that we are to defend)
		opp_food = self.getFoodYouAreDefending(gameState).asList() 

		# Calculating the distance to the visible opponent
		enemy_x = [gameState.getAgentState(a) for a in self.getOpponents(gameState)]
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
				self.timer = 20


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


	def getWeights(self, gameState):
		return {'numInvaders': -1000, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}


class Offensive_Agent(CaptureAgent):



	#Initializing 
	def registerInitialState(self, gameState):
		CaptureAgent.registerInitialState(self, gameState)

		#Initialization code
		if self.red:
			cen_x = int((gameState.data.layout.width - 2) / 2)
		else:
			cen_x = int((gameState.data.layout.width - 2) / 2) + 1
		
		self.boundary = []
		
		for i in range(1, gameState.data.layout.height - 1):
			if not gameState.hasWall(cen_x, i):
				self.boundary.append((cen_x, i))
		self.closestFood = self.get_far_targ(gameState, gameState.getAgentState(self.index).getPosition(), self.getFood(gameState).asList())
		self.randFood = random.choice(self.getFoodYouAreDefending(gameState).asList())
		self.food_counter = 0
		self.opponent = self.getOpponents(gameState)
		self.team = self.getTeam(gameState)
		if self.index == self.team[0]: 
			self.partnerIndex = self.team[1]
		else: 
			self.partnerIndex = self.team[0]

	#helper functions

	def get_closest_targ(self, gameState, position, targets):
		minDistance, nearestTarget = min([(self.getMazeDistance(position, target), target) for target in targets])
		return (minDistance, nearestTarget)
	
	def get_far_targ(self, gameState, position, targets):
		maxDistance, furthestTarget = max([(self.getMazeDistance(position, target), target) for target in targets])
		return furthestTarget

	def getSuccessor(self, gameState, action):
		"""
		Finds the position of next successor
		"""
		successor = gameState.generateSuccessor(self.index, action)
		position = successor.getAgentState(self.index).getPosition()

		if position != nearestPoint(position):
			
			return successor.generateSuccessor(self.index, action)
		else:
			return position

	def getBestAction(self, gameState, targetPos, actions):

		minDist, b_act = min([(self.getMazeDistance(self.getSuccessor(gameState, action), targetPos), action) for action in actions]) 
		#print(action)
		return (minDist, b_act)

	def avoid_one_gh(self, gameState, depth, oppPos):

		state = gameState.deepCopy()
				
		if depth == 0:
			#print("one ghost avoid")
			return self.getMazeDistance(state.getAgentPosition(self.index), oppPos)
		else: 
			actions = state.getLegalActions(self.index)
			disToGhost = [self.avoid_one_gh(state.generateSuccessor(self.index, action), depth - 1, oppPos) for action in actions]
			return sum(disToGhost)/len(disToGhost)

	def avoid_two_gh(self, gameState, depth, opp1Pos, opp2Pos):
		
		state = gameState.deepCopy()
		#print("2 ghost avoid")
		if depth == 0:
			return self.getMazeDistance(state.getAgentPosition(self.index), opp1Pos) + self.getMazeDistance(state.getAgentPosition(self.index), opp2Pos)
		else: 
			actions = state.getLegalActions(self.index)
			disToGhost = [self.avoid_two_gh(state.generateSuccessor(self.index, action), depth - 1, opp1Pos, opp2Pos) for action in actions]
			return sum(disToGhost)/len(disToGhost)			

	def get_act_ghost_one(self, gameState, oppPos, actions):
		maxDist, b_act = max([(self.avoid_one_gh(gameState.generateSuccessor(self.index, action), 3, oppPos), action) for action in actions]) 
		return b_act
	
	def get_act_ghost_two(self, gameState, opp1Pos, opp2Pos, actions):
		maxDis, b_act = max([(self.avoid_two_gh(gameState.generateSuccessor(self.index, action), 3, opp1Pos, opp2Pos), action) for action in actions]) 
		return b_act

	def at_Boundary(self, gameState):
		myPosition = gameState.getAgentState(self.index).getPosition()
		if myPosition in self.boundary: 
			return True
		else: 
			return False
			


	# Function to choose next action
	def chooseAction(self, gameState):


		x, y = gameState.getAgentState(self.index).getPosition()
		myPos = (int(x), int(y))
		actions = gameState.getLegalActions(self.index)

		if len(actions) > 0:
			actions.remove(Directions.STOP)
		
		food_list = self.getFood(gameState).asList()  
		capsules = self.getCapsules(gameState)
		food_list += capsules
		partnerPos = gameState.getAgentState(self.partnerIndex).getPosition()


		if self.closestFood not in food_list: 
			mindis, self.closestFood = self.get_closest_targ(gameState, myPos, food_list)

		if len(food_list) > 2: 
			#While we still have to collect food pallets
			scaredTimes = [gameState.getAgentState(i).scaredTimer for i in self.opponent]

			opponentGhosts = [i for i in self.opponent if not gameState.getAgentState(i).isPacman]
			opponentConfig = [gameState.getAgentState(i).configuration for i in opponentGhosts]


			if len(opponentGhosts) == 2: 
				#print("two ghosts")
				opponent1 = opponentConfig[0]
				opponent2 = opponentConfig[1]

				#This variable will track whether we are being chased or not
				chased_ghost=False

				if opponent1 is not None and opponent2 is not None and (scaredTimes[0] <= 5 or scaredTimes[1] <= 5): 
					opponent1Pos = opponent1.getPosition()
					opponent2Pos = opponent2.getPosition()

					#If power pellets are available
					
					if len(capsules) > 0:
						#Finding the distance to the capsules
						distToCap, nearestCapsule = self.get_closest_targ(gameState, myPos, capsules)

						# Go for the capsule, if ghosts are farther than the capsule
						if distToCap < self.getMazeDistance(opponent1Pos, nearestCapsule) & distToCap < self.getMazeDistance(opponent2Pos, nearestCapsule):
							minDis, action = self.getBestAction(gameState, nearestCapsule, actions)
							return action

					# If capsule is farther away, finding the distance to the closest ghost
					ghostDis=min(self.getMazeDistance(myPos, opponent1Pos),self.getMazeDistance(myPos, opponent2Pos))

					#We find if the PacMan is being chased by a ghost
					last_pos = self.getPreviousObservation() #Previous Game State

					myPos = gameState.getAgentState(self.index).getPosition() #Current Position of the agent
					if last_pos != None:
						#Finding location of the ghosts in previous game state

						enemiesLast = [last_pos.getAgentState(i) for i in self.getOpponents(gameState)]
						chas_gh = []
						
						for i in enemiesLast:
							if (i.getPosition() != None) and (not i.isPacman) and (self.getMazeDistance(myPos,i.getPosition()) < 5) and (i.scaredTimer<5):
								#Finding the Opponent objects that can be chasing
								chas_gh.append(i)
						#print((chas_gh))
						if len(chas_gh) > 0:
						# being chased
							lastDis=min(self.getMazeDistance(i.getPosition(),myPos) for i in chas_gh)
							#print(lastDis)

							if lastDis-ghostDis<=1 and ghostDis<3:
								chased_ghost=True


					#If we are being chased, and the closest ghost is at a distance of 3 or less.
					if ghostDis <= 4 and chased_ghost:
						#If we are pacman
						#print("this runs")
						if gameState.getAgentState(self.index).isPacman:
							minDis, nearexit = self.get_closest_targ(gameState, myPos, self.boundary)
							minDis, action = self.getBestAction(gameState, nearexit, actions)
							return action
						
						# if we are a ghost
						else: 

							if self.food_counter == 0 and self.at_Boundary(gameState): 
								if len(self.getFoodYouAreDefending(gameState).asList()) > 0: 
									self.randFood = random.choice(self.getFoodYouAreDefending(gameState).asList())
								minDis, action = self.getBestAction(gameState, self.randFood, actions)
								self.food_counter = 6
								#print(minDis,action)
								return action
							# If both ghosts are close to each other
							if self.getMazeDistance(myPos, partnerPos) <= 7: 
								if self.index == self.team[0]:
									action = self.get_act_ghost_two(gameState, opponent1Pos, opponent2Pos, actions)
									print("I run")
									return action
							if self.food_counter == 0: 
								if len(self.getFoodYouAreDefending(gameState).asList()) > 0: 
									self.randFood = random.choice(self.getFoodYouAreDefending(gameState).asList())
								minDis, action = self.getBestAction(gameState, self.randFood, actions)
								self.food_counter = 6
								#print("life's good")
								return action
							else: 
								minDis, action = self.getBestAction(gameState, self.randFood, actions)
								self.food_counter -= 1
								#print("This works")
								return action
			
			#If there's one ghost and one pacman
			elif len(opponentGhosts) == 1: 
				#print("one ghost ")
				opponent = opponentConfig[0]
				if gameState.getAgentState(opponentGhosts[0]).scaredTimer <= 5  and opponent is not None:
					opponentPos = opponent.getPosition()
					#Again, we try to get to the capsule if possible
					if len(capsules) > 0:
						distToCap, nearestCapsule = self.get_closest_targ(gameState, myPos, capsules)
						if distToCap < self.getMazeDistance(opponentPos, nearestCapsule):
							minDis, action = self.getBestAction(gameState, nearestCapsule, actions)
							return action
					
					if self.getMazeDistance(myPos, opponentPos) <= 4:
						if gameState.getAgentState(self.index).isPacman: 
							minDis, nearestDoor = self.get_closest_targ(gameState, myPos, self.boundary)
							minDis, action = self.getBestAction(gameState, nearestDoor, actions)
							#print( action)
							return action
						else: 
							if self.getMazeDistance(myPos, partnerPos) <= 7: 
								if self.index == self.team[0]: 
									action = self.get_act_ghost_one(gameState, opponentPos, actions)
									#print(action)
									return action
							
							if self.at_Boundary(gameState) and self.food_counter == 0: 
								if len(self.getFoodYouAreDefending(gameState).asList()) > 0: 
									self.randFood = random.choice(self.getFoodYouAreDefending(gameState).asList())
								minDis, action = self.getBestAction(gameState, self.randFood, actions)
								self.food_counter = 4
								#print(minDis, action)
								return action
							
							if self.food_counter == 0:
								if len(self.getFoodYouAreDefending(gameState).asList()) > 0: 
									self.randFood = random.choice(self.getFoodYouAreDefending(gameState).asList())
								minDis, action = self.getBestAction(gameState, self.randFood, actions)
								self.food_counter = 4
								return action
							else: 
								minDis, action = self.getBestAction(gameState, self.randFood, actions)
								self.food_counter -= 1
								return action
			
			if self.food_counter > 0: 
				minDis, action = self.getBestAction(gameState, self.randFood, actions)
				self.food_counter -= 1
				return action
			
			partnerMinDisttoFood, partnerNearestFood = self.get_closest_targ(gameState, partnerPos, food_list)
			myMinDisttoFood, myNearestFood = self.get_closest_targ(gameState, myPos, food_list)
			minDisttoHome, nearestDoor = self.get_closest_targ(gameState, myPos, self.boundary)
			
			if gameState.getAgentState(self.index).numCarrying > minDisttoHome: 
				minDis, action = self.getBestAction(gameState, nearestDoor, actions)
				return action
			self.closestFood = myNearestFood
			minDis, action = self.getBestAction(gameState, self.closestFood, actions)
			return action
		
		else: #If we have collected (total - 2 ) food pallets, we return back
			minDis, nearestDoor = self.get_closest_targ(gameState, myPos, self.boundary)
			minDis, action = self.getBestAction(gameState, nearestDoor, actions)
			return action
