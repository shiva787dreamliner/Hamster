import sys
import time
import threading
import Queue
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm

gRobotList = []
gQuit = False
class Event(object):
	def __init__(self, eventType, eventData):
		self.eventType = eventType
		self.eventData = eventData	
'''class stateQ(object):
	def __init__(self):
		self.stateQ = Queue.Queue()

	def addToQueue(event):
		self.stateQ.append(event)

	def removeFirstFromQueue():
		self.stateQ.get()'''


class finiteStateMachine(threading.Thread):
	def __init__(self, stateQ):
		super(finiteStateMachine, self).__init__()
		self.currentState = "movingForward"
		self.stateQ = stateQ
		self.stateList = []

	def addState(self, state, event, callBack, nextState):
		self.stateList.append([state, event, callBack, nextState])
	
	def run(self):
		while(True):
			if not self.stateQ.empty():
				print "length of event queue: ", self.stateQ.qsize()
				event = self.stateQ.get()
				for state in self.stateList:
					if state[0] == self.currentState and state[1] == event.eventType:
						print "previous state", state[0]
						state[2]()
						self.currentState = state[3]
						print "new state", state[3]
						break

class checkInput(threading.Thread):
	def __init__(self, stateQ):
		super(checkInput, self).__init__()
		self.stateQ = stateQ
	def run(self):
		while (True):
			for robot in gRobotList:
				proxL = robot.get_proximity(0)
				proxR = robot.get_proximity(1)

				if (robot.get_floor(1) < 20 or robot.get_floor(0) < 20):
					boundryEvent = Event("boundryLine", [proxL, proxR])
					self.stateQ.put(boundryEvent)
					print "qsize in boundry", self.stateQ.qsize()
				elif (proxR < 20 and proxL < 20):
					clearEvent = Event("clear", [proxL, proxR])
					self.stateQ.put(clearEvent)
					print "qsize in clear", self.stateQ.qsize()
				elif (proxR > 30):
					rightObsEvent = Event("rightObstacle", [proxL, proxR])
					self.stateQ.put(rightObsEvent)
					print "qsize in rObs", self.stateQ.qsize()
				elif (proxR - proxL < 20 and proxR > 40 and proxL > 40):
					straObsEvent = Event("straightObstacle", [proxL, proxR])
					self.stateQ.put(straObsEvent)
				elif (proxL > 30):
					leftObsEvent = Event("leftObstacle", [proxL, proxR])
					self.stateQ.put(leftObsEvent)
					print "qsize in leftObs", self.stateQ.qsize()
			time.sleep(0.1)

class HamsterBehvaior(object):
	def __init__(self, stateMachine):
		self.stateMachine = stateMachine
		print "in init"

		self.stateMachine.addState("movingForward", "rightObstacle", self.turnRight, "DetectingObject")
		self.stateMachine.addState("movingForward", "leftObstacle", self.turnLeft, "DetectingObject")
		self.stateMachine.addState("movingForward", "straightObstacle", self.moveForward, "DetectingObject")
		self.stateMachine.addState("movingForward", "boundryLine", self.atBoundry, "movingForward")
		self.stateMachine.addState("movingForward", "clear", self.moveForward, "movingForward")

		self.stateMachine.addState("DetectingObject", "rightObstacle", self.turnRight, "DetectingObject")
		self.stateMachine.addState("DetectingObject", "leftObstacle", self.turnLeft, "DetectingObject")
		self.stateMachine.addState("DetectingObject", "straightObstacle", self.moveForward, "PushingTrash")
		self.stateMachine.addState("DetectingObject", "boundryLine", self.atBoundry, "movingForward")
		self.stateMachine.addState("DetectingObject", "clear", self.moveForward, "movingForward")

		self.stateMachine.addState("PushingTrash", "rightObstacle", self.turnRight, "DetectingObject")
		self.stateMachine.addState("PushingTrash", "leftObstacle", self.turnLeft, "DetectingObject")
		self.stateMachine.addState("PushingTrash", "straightObstacle", self.moveForward, "PushingTrash")
		self.stateMachine.addState("PushingTrash", "boundryLine", self.depositTrash, "movingForward")
		self.stateMachine.addState("PushingTrash", "clear", self.moveForward, "movingForward")



	def moveForward(self):
		for robot in gRobotList:
			robot.set_wheel(0, 50)
			robot.set_wheel(1, 50)
			print "MOVING FORWARD"

	def turnRight(self):
		for robot in gRobotList:
			robot.set_led(1, 3)
			robot.set_led(0, 3)
			robot.set_wheel(0, 2*robot.get_proximity(1)) #have to put actual readings from proximity sensors
			robot.set_wheel(1, robot.get_proximity(0))
			print "TURNING RIGHT"

	def turnLeft(self):
		for robot in gRobotList:
			robot.set_led(1, 1)
			robot.set_led(0, 1)
			robot.set_wheel(1, 2*robot.get_proximity(0)) #have to put actual readings from proximity sensors
			robot.set_wheel(0, robot.get_proximity(1))
			print "TURNING LEFT"

	def atBoundry(self):
		for robot in gRobotList:
			robot.set_wheel(1, 100) #have to put actual readings from proximity sensors
			robot.set_wheel(0, -100)
			print "IN AT BOUNDRY"

	def depositTrash(self):
		for robot in gRobotList:
			robot.set_wheel(1, 50) #have to put actual readings from proximity sensors
			robot.set_wheel(0, 50)
			robot.set_musical_note(40)
			robot.set_led(1, 2)
			robot.set_led(0, 2)
			time.sleep(1)
			robot.set_musical_note(0)
			robot.set_wheel(1, 0)
			robot.set_wheel(0, 100)
			print "DEPOSITING TRASH"



def main(): 
	robotComm = RobotComm(1)
	commCheck = False
	commEst = False

	stateQ = Queue.Queue()

	global gRobotList
	robotComm.start() #starts comm thread 
	print "Bluetooth connected"
	gRobotList = robotComm.robotList


	frame = tk.Tk()

	stateMachine = finiteStateMachine(stateQ)
	stateMachine.daemon = True
		
	# print "creating behavior"
	behavior = HamsterBehvaior(stateMachine)
	stateMachine.start()



	monitorInput = checkInput(stateQ)
	monitorInput.daemon = True
	monitorInput.start()
	
	frame.mainloop()

	#robotComm.stop()
	print "terimanted"

if __name__ == "__main__":
	main()