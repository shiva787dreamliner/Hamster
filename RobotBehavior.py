import sys
import time

class finiteStateMachine():
	def __init__(self, path, graph, startNode, goalNode, gRobotList):
		self.stateList = []
		self.currentState = "forwardFacing"
		self.robotBeh = RobotBehavior(path, graph, startNode, goalNode, gRobotList)

		self.robotBeh.conversionToMovements()
		self.robotMovements = self.robotBeh.robotMovements

		self.addState("forwardFacing", "forward", self.robotBeh.moveForward, "forwardFacing")
		self.addState("forwardFacing", "right", self.robotBeh.moveRight, "rightFacing")
		self.addState("forwardFacing", "left", self.robotBeh.moveLeft, "leftFacing")
		self.addState("forwardFacing", "backward", self.robotBeh.moveBackward, "backwardFacing")

		self.addState("rightFacing", "forward", self.robotBeh.moveLeft, "forwardFacing")
		self.addState("rightFacing", "right", self.robotBeh.moveForward, "rightFacing")
		self.addState("rightFacing", "left", self.robotBeh.moveBackward, "leftFacing")
		self.addState("rightFacing", "backward", self.robotBeh.moveRight, "backwardFacing")

		self.addState("leftFacing", "forward", self.robotBeh.moveRight, "forwardFacing")
		self.addState("leftFacing", "right", self.robotBeh.moveBackward, "rightFacing")
		self.addState("leftFacing", "left", self.robotBeh.moveForward, "leftFacing")
		self.addState("leftFacing", "backward", self.robotBeh.moveLeft, "backwardFacing")

		self.addState("backwardFacing", "forward", self.robotBeh.moveBackward, "forwardFacing")
		self.addState("backwardFacing", "right", self.robotBeh.moveLeft, "rightFacing")
		self.addState("backwardFacing", "left", self.robotBeh.moveRight, "leftFacing")
		self.addState("backwardFacing", "backward", self.robotBeh.moveForward, "backwardFacing")


	def addState(self, state, event, callBack, nextState):
		self.stateList.append([state, event, callBack, nextState])

	def executingFSM(self):
		print "inside FSM"
		for action in self.robotMovements:
			# print "inside for loop"
			#if not self.stateQ.empty():
			#print "length of event queue: ", self.stateQ.qsize()
			for state in self.stateList:
				# print len(self.stateList)
				# print "inside the inner loop"
				if state[0] == self.currentState and state[1] == action:
					# print "inside  the if statement"
					#print "previous state", state[0]
					state[2]()
					self.currentState = state[3]
					#print "new state", state[3]
					break


class RobotBehavior (object):
	def __init__(self, path, graph, startNode, goalNode, gRobotList):
		self.path = path
		self.robotMovements = []
		self.graph = graph
		self.startNode = startNode
		self.goalNode = goalNode
		self.gRobotList = gRobotList

		# self.fsm.addState("forwadFacing", "forward", self.moveForward, "forwardFacing")
		# self.fsm.addState("forwadFacing", "right", self.moveRight, "rightFacing")
		# self.fsm.addState("forwadFacing", "left", self.moveLeft, "leftFacing")
		# self.fsm.addState("forwadFacing", "backward", self.moveBackward, "backwardFacing")

		# self.fsm.addState("rightFacing", "forward", self.moveLeft, "forwardFacing")
		# self.fsm.addState("rightFacing", "right", self.moveForward, "rightFacing")
		# self.fsm.addState("rightFacing", "left", self.moveBackward, "leftFacing")
		# self.fsm.addState("rightFacing", "backward", self.moveRight, "backwardFacing")

		# self.fsm.addState("leftFacing", "forward", self.moveRight, "forwardFacing")
		# self.fsm.addState("leftFacing", "right", self.moveBackward, "rightFacing")
		# self.fsm.addState("leftFacing", "left", self.moveForward, "leftFacing")
		# self.fsm.addState("leftFacing", "backward", self.moveLeft, "backwardFacing")

		# self.fsm.addState("backwardsFacing", "forward", self.moveBackward, "forwardFacing")
		# self.fsm.addState("backwardsFacing", "right", self.moveLeft, "rightFacing")
		# self.fsm.addState("backwardsFacing", "left", self.moveRight, "leftFacing")
		# self.fsm.addState("backwardsFacing", "backward", self.moveForward, "backwardFacing")

	def conversionToMovements(self):
		previousNodeName = self.startNode
		currentNodeName = ""

		for node in self.path:
			currentNodeName = node
			currentX, currentY = self.conversionToCoord(currentNodeName)
			pastX, pastY = self.conversionToCoord(previousNodeName)
			
			if (currentX - pastX > 0):
				self.robotMovements.append("right")
			elif (currentX - pastX < 0):
				self.robotMovements.append("left")
			elif (currentY - pastY > 0):
				self.robotMovements.append("backward")
			elif (currentY - pastY < 0):
				self.robotMovements.append("forward")

			previousNodeName = currentNodeName

	def conversionToCoord(self, nodeName):
		index = 0
		for i in range (len(nodeName)):
			if nodeName[i] == ",":
				index = i 
		#print index
		x = int(nodeName[:index]) + 1
		y = int(nodeName[index+1:]) + 1

		return x,y

	def moveForward(self):
		print "is moving Forward"
		for robot in self.gRobotList:
			while not self.checkIfNode():
				# print "in move Forward loop"
				robot.set_led(0, 3)
				robot.set_led(1, 3)
				totalErrorPID = self.proportion(robot)
				totalErrorPID = totalErrorPID
				robot.set_wheel(0, int(robot.get_floor(0) + totalErrorPID))
				robot.set_wheel(1, int(robot.get_floor(1) - totalErrorPID))
				# robot.set_wheel(0, 50)
				# robot.set_wheel(1, 50)

	def moveRight(self):
		print "is moving right"
		for robot in self.gRobotList:
			robot.set_wheel(0, 40)
			robot.set_wheel(1, -40)
			time.sleep(0.7)
			# robot.set_wheel(0, 0)
			# robot.set_wheel(1, 0)
			while not self.checkIfNode():
				self.moveForward()
				#print "in moving forward loop"

	def moveLeft(self):
		print "is moving left"
		for robot in self.gRobotList:
			robot.set_wheel(0, -40)
			robot.set_wheel(1, 40)
			time.sleep(0.7)
			robot.set_wheel(0, 0)
			robot.set_wheel(1, 0)
			#print "getting to the checking node place"
			print self.checkIfNode()
			while not self.checkIfNode():
				#self.moveForward()
				pass

	def moveBackward(self):
		print "is moving back"
		for robot in self.gRobotList:
			robot.set_wheel(0, 50)
			robot.set_wheel(1, -50)
			time.sleep(1.4)
			while not self.checkIfNode():
				self.moveForward()

	def proportion(self, robot):
		floorL = robot.get_floor(0)
		floorR = robot.get_floor(1)

		pConstant = 0.02

		currentError = floorL - floorR

		# print "floor l/r", floorL, floorR
		# print "proportional error", currentError

		'''leftError = 100 - floorL
		rightError = 100 - floorR

		if (leftError <= 5 and rightError <= 5):
			robot.set_wheel(1, 20)
			robot.set_wheel(0, 20)
		else:
			robot.set_wheel(1, int(leftError * 2))
			robot.set_wheel(0, int(rightError* 2))'''
		return currentError * pConstant

	def checkIfNode(self): #Return true or false
		for robot in self.gRobotList:
			if (robot.get_floor(1) < 30 and robot.get_floor(0) < 30):
				robot.set_musical_note(40)
				robot.set_musical_note(0)
				return True
			else:
				return False





