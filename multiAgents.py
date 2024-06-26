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
import random, util

from game import Agent

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

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()

        # calculate the food distance and letting the pacman moving toward the foods 
        foodDistance = [manhattanDistance(newPos, food) for food in newFood.asList()]
        if foodDistance:
            score += 1.0/min(foodDistance) #letting the pacman moving twoard the most closest food 

        # calculate teh ghost distance and letting the pacman move away from the ghost
        ghostDistance = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        if ghostDistance and min(ghostDistance) < 2 :   #if the pacman has the distance that is less than 2 to the ghost
            score -= 200        #subtract a large value of score to allow the pacman moving away from the ghost

        return score

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
        _, action = self.minimax(gameState, 0, 0) 
        return action
    
    #the function would return a pair minimax value and action
    def minimax(self, gameState, depth, index):
        #recursion check if the game is over, it would evaluate the game state using the evaluationFunction and return the result of the game 
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        
        #get the next agent index and the depth
        nextIndex = (index + 1) % gameState.getNumAgents()
        nextDepth = depth

        if nextIndex == 0:
            nextDepth += 1
        
        actions = gameState.getLegalActions(index)
        if index == 0: #max agent for the pacman
            return max((self.minimax(gameState.generateSuccessor(index, action), nextDepth, nextIndex)[0], action) for action in actions)
        else: #min agent for the ghost 
            return min((self.minimax(gameState.generateSuccessor(index, action), nextDepth, nextIndex)[0], action) for action in actions)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        _, action = self.alphaBetaPruning(gameState, 0, 0, -float('inf'), float('inf'))
        return action

    def alphaBetaPruning(self, gameState, depth, index, alpha, beta):
        #recursion check if the game is over, it would evaluate the game state using the evaluationFunction and return the result of the game 
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        
        #get the next agent index and the depth
        nextIndex = (index + 1) % gameState.getNumAgents()
        nextDepth = depth

        if nextIndex == 0:
            nextDepth += 1

        actions = gameState.getLegalActions(index)
        #alpha (max best option on path to root)
        if index == 0 : 
            value = -float ('inf') #initialize v = -∞
            for action in actions: # for each successor of state
                newValue, _ = self.alphaBetaPruning(gameState.generateSuccessor(index, action), nextDepth, nextIndex, alpha, beta)
                if (newValue > value):
                    value, betterAction = newValue, action
                if(value > beta): #if v > beta return v
                    return value, betterAction
                alpha = max(alpha, value) #alpha = max (a,v)
            return value, betterAction
        else: #beta (min best option on path to root)
            value = float('inf') #initialize v = +∞
            for action in actions: # for each successor of state
                newValue, _ = self.alphaBetaPruning(gameState.generateSuccessor(index, action), nextDepth, nextIndex, alpha, beta)
                if (newValue < value):
                    value, betterAction = newValue, action
                if(value < alpha): #if v < alpha return v
                    return value, betterAction
                beta = min(beta, value) #beta = max (b,v)
            return value, betterAction


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
        _, action = self.expectimax(gameState, 0, 0, )
        return action
    
    def expectimax(self, gameState, depth, index):
        #recursion check if the game is over, it would evaluate the game state using the evaluationFunction and return the result of the game 
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
             return self.evaluationFunction(gameState), None
        
        #get the next agent index and the depth
        nextIndex = (index + 1) % gameState.getNumAgents()
        nextDepth = depth

        if nextIndex == 0:
            nextDepth += 1

        #get the legal action form the current agen can take from the current game state 
        actions = gameState.getLegalActions(index)

        if index == 0: # same max agent for the pacman
            return max((self.expectimax(gameState.generateSuccessor(index, action), nextDepth, nextIndex)[0], action) for action in actions)
        else: #expectation agent for the ghost 
            #calculate the sum of expectimax value of possible actions for the ghost
            expectation = sum((self.expectimax(gameState.generateSuccessor(index, action), nextDepth, nextIndex)[0]) for action in actions)
            expectation /= len(actions)
            return expectation, None
            

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostState = currentGameState.getGhostStates()
    score = currentGameState.getScore()

    # CONST negative infinite value
    INFINITE = -float('inf')

    #checks the distance for the cloest food
    foodDistances = [util.manhattanDistance(position, foodPosition) for foodPosition in food.asList()]

    #check the length to see if the food distances is greater then 0
    if len(foodDistances) > 0:
        score += 10.0 / min(foodDistances)
    else:
        score += 10.0

    #checks the distance to the ghost
    for ghost in ghostState:
        dis = manhattanDistance(position, ghost.getPosition())
        if dis > 0:
            #check if the ghost is scared, add point if it does, - point if it doesn't
            if ghost.scaredTimer > 0:
                score += (100.0) / dis
            else:
                score += (-10) / dis
        else:
            return INFINITE
    
    return score

# Abbreviation
better = betterEvaluationFunction
