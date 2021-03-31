# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        # mdp.getStates()
        # mdp.getPossibleActions(state)
        # mdp.getTransitionStatesAndProbs(state, action)
        # mdp.getReward(state, action, nextState)
        # mdp.isTerminal(state)
        "*** YOUR CODE HERE ***"

        x_states = self.mdp.getStates()
        x_iter = self.iterations

        #Looping over the no. of iterations
        for i in range(x_iter):

          i_vals = self.values.copy()

          for j in x_states:

            if not self.mdp.isTerminal(j):
              j_action = self.getAction(j)
              i_vals[j] = self.computeQValueFromValues(j, j_action)
          self.values = i_vals


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)          
        """
        "*** YOUR CODE HERE ***"
        prob_of_transition = self.mdp.getTransitionStatesAndProbs(state, action)
        q_val = 0
        for x in prob_of_transition:
          x_state, x_prob = x
          # Finding the reward for the state
          # The getReward is implemented as - getReward(self, state, action, nextState)
          x_reward = self.mdp.getReward(state, action, x_state)
          x_val = self.getValue(x_state)
          x_disc = self.discount
          #Calculating the Q Value from Tranition probability, reward, discount and Value
          q_val += x_prob*(x_reward + (x_val*x_disc))

        return q_val

        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Checking if Terminal State, then return None
        if (self.mdp.isTerminal(state)): 
          return None
        # If not terminal state, returning
        else:
          x_dict = util.Counter() 

          
          x_actions = self.mdp.getPossibleActions(state)
          for action in x_actions:
            x_dict[action] = self.computeQValueFromValues(state, action)

          max_qval = x_dict.argMax() #Finding the action with maximum qVal
          #print(x_dict)
          #print(max_qval)
          return max_qval
          
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #implementing the asynchronous value iteration agent, updating one state per iteration
        #Getting the current state first

        x_state= self.mdp.getStates()
        x_iter = self.iterations
        #print(x_state)
        for i in range(x_iter):
          x_vals = self.values.copy()
          #Picking the ith state so that we iterate over it 
          i_state = x_state[i%len(x_state)]
          #Checking if the state is terminal state
          if not self.mdp.isTerminal(i_state):
            #if not terminal state, finding the action, and calcualting the value iteration
            i_action = self.getAction(i_state)
            x_vals[i_state] = self.computeQValueFromValues(i_state, i_action)
          self.values = x_vals

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #We will start with defining a variable to store predecessors of a state
        x_pred = {} #defining as a set
        # Finding all states that have a nonzero probability of reaching the current state
        for x_state in self.mdp.getStates():
          x_pred[x_state] = set() 
        for x_state in self.mdp.getStates():

          for x_action in self.mdp.getPossibleActions(x_state):
            for nxt_state, state_prob in self.mdp.getTransitionStatesAndProbs(x_state, x_action):
              #Checking if the state has non-zero probability
              if state_prob >0: 
                #If non-zero probability, add to predecessors set
                y_pred = x_pred[nxt_state]
                y_pred.add(x_state)
                x_pred[nxt_state] = y_pred

        # Now that we have computed predessors of all states, we will initialize a priority queue
        priority_q = util.PriorityQueue()

        #Now, we will iterate over non-terminal states
        for y_state in self.mdp.getStates():
          if not self.mdp.isTerminal(y_state):
            #Initializing qvalue variable to negative infinity
            max_qval = float('-inf')

            for y_action in self.mdp.getPossibleActions(y_state):
              # Checking if the QValue of the current state action pair is greater than max_qval
              # and updating max_qval if that's the case
              y_qval = self.computeQValueFromValues(y_state, y_action)
              if (max_qval < y_qval ):
                max_qval = y_qval

            if max_qval == float('-inf'):

              diff =  self.values[y_state]
            else:
              #Finding the absolute differnce between the current state value and the max QVal
              diff = abs(self.values[y_state] - max_qval)
            # Pushing the absolute difference to the priority queue
            priority_q.push(y_state , -diff)

            #Iterating over the no.of iterations
        for i in range(self.iterations):
              #Checking if the priority queue is empty, and terminating if true
          if priority_q.isEmpty():
            return

          # Popping the state S from the Priority Queue
          i_state = priority_q.pop()

          #Updating the value of i_state if it's not a terminal state
          if not self.mdp.isTerminal(i_state):
            #Updating the value of i_state in self.values
            i_action = self.computeActionFromValues(i_state)
            self.values[i_state] = self.computeQValueFromValues(i_state, i_action)

          # Looping over the predecessors of i_state
          for pred_i in x_pred[i_state]:
            if not self.mdp.isTerminal(pred_i):
              max_qval = float('-inf')

              for y_action in  self.mdp.getPossibleActions(pred_i):
                y_qval = self.computeQValueFromValues(pred_i, y_action)
                if (max_qval < y_qval):
                  max_qval = y_qval
                #Calculating the absolute differce between current value of pred_i and max_qval
              if max_qval == float('-inf'):
                diff = abs(self.values[pred_i])
              else: 
                diff = abs(self.values[pred_i] - max_qval)
                #Pusing the predecessor to the priority queue if the difference is greater than theta
              if (diff > self.theta):
                  #Updating the priority , if pred_i already exists
                priority_q.update(pred_i, -diff)






