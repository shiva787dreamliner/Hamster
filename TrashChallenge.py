import sys
import time
import threading
import Queue
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm

gRobotList = []
gQuit = False
#flag it as global here?
gstateQue = Queue.Queue()
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
			print "in thread fsm"
			if not self.stateQ.empty():
				event = self.stateQ.get()
				for state in self.stateList:
					if state[0] == self.currentState and state[1] == event.eventType:
						state[2]
						self.currentState = state[3]
						break

class checkInput(threading.Thread):
	def __init__(self, stateQ):
		super(checkInput, self).__init__()
		self.stateQ = stateQ
	def run(self):
		while (True):
			#print "qsize", gstateQue.qsize()
			for robot in gRobotList:
				proxL = robot.get_proximity(0)
				proxR = robot.get_proximity(1)

				if (robot.get_floor(1) < 10 or robot.get_floor(0) < 10):
					boundryEvent = Event("boundryLine", [proxL, proxR])
					self.stateQ.put(boundryEvent)
					#print "qsize", gstateQue.qsize()
				elif (proxR < 20 and proxL < 20):
					clearEvent = Event("clear", [proxL, proxR])
					self.stateQ.put(clearEvent)
					#print "qsize", gstateQue.qsize()
				elif (proxR > proxL):
					rightObsEvent = Event("rightObstacle", [proxL, proxR])
					self.stateQ.put(rightObsEvent)
					#print "qsize", gstateQue.qsize()
				elif (proxL > proxR):
					leftObsEvent = Event("leftObstacle", [proxL, proxR])
					self.stateQ.put(leftObsEvent)
					#print "qsize", gstateQue.qsize()

class HamsterBehvaior(object):
	def __init__(self, stateMachine):
		self.stateMachine = stateMachine
		print "in init"
		for robot in gRobotList:
			self.robot = robot
			print "robot initialized"
		print "after init"

		self.stateMachine.addState("movingForward", "rightObstacle", self.turnRight, "DetectingObject")
		self.stateMachine.addState("movingForward", "leftObstacle", self.turnLeft, "DetectingObject")
		self.stateMachine.addState("movingForward", "boundryLine", self.atBoundry, "movingForward")
		self.stateMachine.addState("movingForward", "clear", self.moveForward, "movingForward")

		self.stateMachine.addState("DetectingObject", "rightObstacle", self.moveForward, "PushingTrash")
		self.stateMachine.addState("DetectingObject", "leftObstacle", self.moveForward, "PushingTrash")
		self.stateMachine.addState("DetectingObject", "boundryLine", self.atBoundry, "movingForward")
		self.stateMachine.addState("DetectingObject", "clear", self.moveForward, "movingForward")

		self.stateMachine.addState("PushingTrash", "rightObstacle", self.moveForward, "PushingTrash")
		self.stateMachine.addState("PushingTrash", "leftObstacle", self.moveForward, "PushingTrash")
		self.stateMachine.addState("PushingTrash", "boundryLine", self.depositTrash, "selfForward")
		self.stateMachine.addState("PushingTrash", "clear", self.moveForward, "movingForward")



	def moveForward():
		self.robot.set_wheel(0, 50)
		self.robot.set_wheel(1, 50)

	def turnRight():
		self.robot.set_wheel(0, 100) #have to put actual readings from proximity sensors
		self.robot.set_wheel(1, 0)

	def turnLeft():
		self.robot.set_wheel(1, 100) #have to put actual readings from proximity sensors
		self.robot.set_wheel(0, 0)

	def atBoundry():
		self.robot.set_wheel(1, 100) #have to put actual readings from proximity sensors
		self.robot.set_wheel(0, 0)

	def depositTrash():
		self.robot.set_wheel(1, 50) #have to put actual readings from proximity sensors
		self.robot.set_wheel(0, 50)
		time.sleep(0.1)
		self.robot.set_wheel(1, 0)
		self.robot.set_wheel(0, 100)



def main(): 
	robotComm = RobotComm(1)
	commCheck = False

	stateQ = Queue.Queue()

	global gRobotList
	robotComm.start() #starts comm thread 
	print "Bluetooth connected"
	gRobotList = robotComm.robotList

	frame = tk.Tk()

	print "state machine created"
	stateMachine = finiteStateMachine(stateQ)
	stateMachine.daemon = True
		
	print "creating behavior"
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