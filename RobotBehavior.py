import sys
import time

class Action(object):
	def __init__(self, type, nodeName, nextNode):
		self.type = type
		self.nodeName = nodeName
		self.nextNode = nextNode

class finiteStateMachine():
	def __init__(self, path, graph, startNode, goalNode, gRobotList, display, bfs):
		self.stateList = []
		self.currentState = "forwardFacing"
		self.robotBeh = RobotBehavior(path, graph, startNode, goalNode, gRobotList, display, bfs)

		self.robotBeh.conversionToMovements()
		self.robotMovements = self.robotBeh.robotMovements
		##print self.robotMovements

		self.addState("forwardFacing", "forward", self.robotBeh.moveForward, "forwardFacing")
		self.addState("forwardFacing", "right", self.robotBeh.moveRight, "rightFacing")
		self.addState("forwardFacing", "left", self.robotBeh.moveLeft, "leftFacing")
		self.addState("forwardFacing", "backward", self.robotBeh.moveBackward, "backwardFacing")
		self.addState("forwardFacing", "end", self.robotBeh.end, "endState")
		#self.addState("forwardFacing", "nodeFound", self.robotBeh.checkForObs, "checkingObs")

		self.addState("rightFacing", "forward", self.robotBeh.moveLeft, "forwardFacing")
		self.addState("rightFacing", "right", self.robotBeh.moveForward, "rightFacing")
		self.addState("rightFacing", "left", self.robotBeh.moveBackward, "leftFacing")
		self.addState("rightFacing", "backward", self.robotBeh.moveRight, "backwardFacing")
		self.addState("rightFacing", "end", self.robotBeh.end, "endState")
		#self.addState("rightFacing", "nodeFound", self.robotBeh.checkForObs, "checkingObs")

		self.addState("leftFacing", "forward", self.robotBeh.moveRight, "forwardFacing")
		self.addState("leftFacing", "right", self.robotBeh.moveBackward, "rightFacing")
		self.addState("leftFacing", "left", self.robotBeh.moveForward, "leftFacing")
		self.addState("leftFacing", "backward", self.robotBeh.moveLeft, "backwardFacing")
		self.addState("leftFacing", "end", self.robotBeh.end, "endState")
		#self.addState("leftFacing", "nodeFound", self.robotBeh.checkForObs, "checkingObs")

		self.addState("backwardFacing", "forward", self.robotBeh.moveBackward, "forwardFacing")
		self.addState("backwardFacing", "right", self.robotBeh.moveLeft, "rightFacing")
		self.addState("backwardFacing", "left", self.robotBeh.moveRight, "leftFacing")
		self.addState("backwardFacing", "backward", self.robotBeh.moveForward, "backwardFacing")
		self.addState("backwardFacing", "end", self.robotBeh.end, "endState")
		#self.addState("backwardFacing", "nodeFound", self.robotBeh.checkForObs, "checkingObs")



	def addState(self, state, event, callBack, nextState):
		self.stateList.append([state, event, callBack, nextState])

	def executingFSM(self):
		#print "inside FSM"
		bool_break = False
		#where the first break is: set it to true & in the first loop do if bool_break break
		while (True):
			#print "this is the robotmovements before the for loop:"
			for acion in self.robotMovements:
				print acion.type
			for action in self.robotMovements:
				# #print "inside for loop"
				#if not self.stateQ.empty():
				##print "length of event queue: ", self.stateQ.qsize()\
				for state in self.stateList:
					# #print len(self.stateList)
					# #print "inside the inner loop"
					if state[0] == self.currentState and state[1] == action.type:
						##print action
						print "previous state", state[0]

						#BELOW IS MOVEMENT
						print "in state machine", action.nodeName
						state[2](True, action.nodeName, self.currentState, action.nextNode)

						#add actions to [] "temp_list"
						self.currentState = state[3]
						print "next state", state[3]
						#you can edit self.robotMovements here
						
						self.robotBeh.conversionToMovements()
						
						self.robotMovements = self.robotBeh.robotMovements
						#print "this is THE NEW robotmovements", self.robotMovements
						for acion in self.robotMovements:
							print acion.type
						#where new movements is "old" movements if no obstacle
						#it's something else if there is one (new path)
						bool_break = True
						break
				if (bool_break):
					#print "in bool break"
					break
			print "at end of fsm", self.robotMovements
			for acion in self.robotMovements:
				print acion.type
		#at this level you can change - robotMovements
		#self.stateList
					##print "new state", state[3]


class RobotBehavior (object):
	def __init__(self, path, graph, startNode, goalNode, gRobotList, display, bfs):
		self.path = path
		self.robotMovements = []
		self.graph = graph
		self.startNode = startNode
		self.goalNode = goalNode
		self.gRobotList = gRobotList
		self.display = display
		self.bfs = bfs

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
		nextNode = ""
		##print self.path
		self.robotMovements = []
		for nodeIndex in range(len(self.path)):
			currentNodeName = self.path[nodeIndex]
			currentX, currentY = self.conversionToCoord(currentNodeName)
			pastX, pastY = self.conversionToCoord(previousNodeName)
			
			print "node, currentNodeName", self.path[nodeIndex], currentNodeName
			# #print "this is the current stuff", currentX, currentY
			# #print "this is the past stuff", pastX, pastY
			
			# if (self.checkIfNode()):
			# 	checkNodeAction = Action("nodeFound", previousNodeName)
			# 	self.robotMovements.append(checkNodeAction)
			# 	#print "putting check node action"
			if (currentX - pastX > 0):
				if (nodeIndex + 1 < len(self.path)):
					nextNode = self.path[nodeIndex + 1]
				rightAction = Action("right", currentNodeName, nextNode)
				self.robotMovements.append(rightAction)
				##print "putting in right action"
			elif (currentX - pastX < 0):
				if (nodeIndex + 1 < len(self.path)):
					nextNode = self.path[nodeIndex + 1]
				leftAction = Action("left", currentNodeName, nextNode)
				self.robotMovements.append(leftAction)
				##print "putting in left action"
			elif (currentY - pastY > 0):
				if (nodeIndex + 1 < len(self.path)):
					nextNode = self.path[nodeIndex + 1]
				backwardAction = Action("backward", currentNodeName, nextNode)
				self.robotMovements.append(backwardAction)
				##print "putting in backward action"
			elif (currentY - pastY < 0):
				if (nodeIndex + 1 < len(self.path)):
					nextNode = self.path[nodeIndex + 1]
				forwardAction = Action("forward", currentNodeName, nextNode)
				self.robotMovements.append(forwardAction)
				##print "putting in forward action"

			previousNodeName = currentNodeName
		

		if (self.path[nodeIndex] == self.goalNode):
			endAction = Action("end", nodeIndex, nextNode)
			self.robotMovements.append(endAction)
			##print "putting in end action"

	def conversionToCoord(self, nodeName):
		index = 0
		for i in range (len(nodeName)):
			if nodeName[i] == ",":
				index = i 
		##print index
		x = int(nodeName[:index])
		y = int(nodeName[index+1:])

		return x,y

	def moveForward(self, actualCallIn, nodeName, state, nextNode):
		actualCall = actualCallIn
		##print "is moving forward FALSE"
		if (actualCall == False):
			for robot in self.gRobotList:
				robot.set_led(0, 3)
				robot.set_led(1, 3)
				totalErrorPID = self.proportion(robot)
				totalErrorPID = totalErrorPID
				robot.set_wheel(0, int(robot.get_floor(0) + totalErrorPID))
				robot.set_wheel(1, int(robot.get_floor(1) - totalErrorPID))
		
		elif (actualCall == True):
			#print "this is the nodeName", nodeName
			for robot in self.gRobotList:
				##print self.checkIfNode()
				while not self.checkIfNode():
					# #print "in move Forward loop"
					##print "is moving Forward TRUE"
					robot.set_led(0, 3)
					robot.set_led(1, 3)
					totalErrorPID = self.proportion(robot)
					totalErrorPID = totalErrorPID * 0.5
					robot.set_wheel(0, int(robot.get_floor(0) + totalErrorPID))
					robot.set_wheel(1, int(robot.get_floor(1) - totalErrorPID))
				# robot.set_wheel(0, 50)
				# robot.set_wheel(1, 50)
				newObsList, removedObsList = self.checkForObs(nodeName, state)
				self.updateGraphBFS(nextNode, newObsList, removedObsList)

	def moveRight(self, actualCallIn, nodeName, state, nextNode):
		#print "is moving right"
		for robot in self.gRobotList:
			robot.set_wheel(0, 40)
			robot.set_wheel(1, -40)
			time.sleep(0.6)
			# robot.set_wheel(0, 0)
			# robot.set_wheel(1, 0)
			# #print self.checkIfNode()
			while not self.checkIfNode():
				self.moveForward(False, nodeName, state, nextNode)
			newObsList, removedObsList = self.checkForObs(nodeName, state)
			self.updateGraphBFS(nextNode, newObsList, removedObsList)


				##print "in moving forward loop"

	def moveLeft(self, actualCallIn, nodeName, state, nextNode):
		#print "is moving left"
		for robot in self.gRobotList:
			robot.set_wheel(0, -40)
			robot.set_wheel(1, 40)
			time.sleep(0.6)
			robot.set_wheel(0, 0)
			robot.set_wheel(1, 0)
			##print "getting to the checking node place"
			# #print self.checkIfNode()
			while not self.checkIfNode():
				self.moveForward(False, nodeName, state, nextNode)
			newObsList, removedObsList = self.checkForObs(nodeName, state)
			self.updateGraphBFS(nextNode, newObsList, removedObsList)


	def moveBackward(self, actualCallIn, nodeName, state, nextNode):
		#print "is moving back"
		for robot in self.gRobotList:
			robot.set_wheel(0, 50)
			robot.set_wheel(1, -50)
			time.sleep(1.4)
			while not self.checkIfNode():
				self.moveForward(False, nodeName, state, nextNode)
			newObsList, removedObsList = self.checkForObs(nodeName, state)
			self.updateGraphBFS(nextNode, newObsList, removedObsList)


	def end(self, actualCallIn, nodeName):
		for robot in self.gRobotList:
			robot.set_wheel(0, 0)
			robot.set_wheel(1, 0)
			robot.set_led(0, 2)
			robot.set_led(1, 2)
			robot.set_musical_note(50)
			time.sleep(0.1)
			robot.set_musical_note(0)

	def proportion(self, robot):
		floorL = robot.get_floor(0)
		floorR = robot.get_floor(1)

		pConstant = 0.02

		currentError = floorL - floorR

		return currentError * pConstant

	def checkIfNode(self): #Return true or false
		for robot in self.gRobotList:
			if (robot.get_floor(1) < 50 and robot.get_floor(0) < 50):
				robot.set_musical_note(40)
				time.sleep(0.1)
				robot.set_musical_note(0)
				# for i in range (4):
				# 	robot.set_wheel(0, 50)
				# 	robot.set_wheel(1, -50)
				# 	self.checkForObs()
				return True
			else:
				return False

	def checkForObs(self, nodeName, state):
		for robot in self.gRobotList:
			newObsList = []
			removedObsList = []
			currentX, currentY = self.conversionToCoord(nodeName)
			
			#CHANGE FROM HARDCODE 
			if (state == "forwardFacing"):
				nearbyCoords = [str(currentX + 1) + "," + str(currentY), str(currentX) + "," + str(currentY + 1), str(currentX - 1) + "," + str(currentY), str(currentX) + "," + str(currentY - 1)]
			elif (state == "leftFacing"):
				nearbyCoords = [str(currentX) + "," + str(currentY - 1), str(currentX + 1) + "," + str(currentY), str(currentX) + "," + str(currentY + 1), str(currentX - 1) + "," + str(currentY)]
			elif (state == "rightFacing"):
				nearbyCoords = [str(currentX) + "," + str(currentY + 1), str(currentX - 1) + "," + str(currentY), str(currentX) + "," + str(currentY - 1), str(currentX + 1) + "," + str(currentY)]
			elif (state == "backwardFacing"):
				nearbyCoords = [str(currentX - 1) + "," + str(currentY), str(currentX) + "," + str(currentY - 1), str(currentX + 1) + "," + str(currentY), str(currentX) + "," + str(currentY + 1)]

			for orientations in range (4):
				robot.set_wheel(0, 40)
				robot.set_wheel(1, -40)
				time.sleep(0.6)
				robot.set_wheel(0, 0)
				robot.set_wheel(1, 0)
				# totalErrorPID = self.proportion(robot)
				# totalErrorPID = totalErrorPID * 0.5
				while not (robot.get_floor(0) - robot.get_floor(1)) < 5 or robot.get_floor(0) - robot.get_floor(1) > -5:
					print "in PID loop"
					totalErrorPID = self.proportion(robot)
					totalErrorPID = totalErrorPID * 30
					print "moving the wheels"
					if (robot.get_floor(0) > robot.get_floor(1)):
						robot.set_wheel(0, int(totalErrorPID))
						robot.set_wheel(1, int(-totalErrorPID))
					elif(robot.get_floor(1) > robot.get_floor(0)):
						robot.set_wheel(0, int(-totalErrorPID))
						robot.set_wheel(1, int(totalErrorPID))
				time.sleep(0.5)
				if (robot.get_proximity(0) > 50 and robot.get_proximity(1) > 50):
					newObsList.append(nearbyCoords[orientations])
					#print "these are the new obstacles", newObsList
				else:
					removedObsList.append(nearbyCoords[orientations])
					#print "these are the removed obstacles", removedObsList
			return newObsList, removedObsList


	def updateGraphBFS(self, nextNode, newObsList, removedObsList):
		newGraph = self.display.updateGraph(newObsList, removedObsList)
		#print "in update Graph bfs new graph", newGraph
		self.bfs.updateGraph(newGraph)
		#print "the nodeName for state in updateGarphBFS",nodeName
		self.path = self.bfs.bfs_shortest_path(nextNode, self.goalNode)
		print self.path
		#print "this is the new path", path
		self.display.highlight_path(self.path)
		self.graph = newGraph
		#self.conversionToMovements()







