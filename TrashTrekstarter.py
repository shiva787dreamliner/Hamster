'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   Stater program of 3-state obstacle avoidance using FSM.

   Name:          starter1.py
   By:            Qin Chen
   Last Updated:  6/10/17

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
import Queue
from HamsterAPI.comm_ble import RobotComm	# no dongle
#from HamsterAPI.comm_usb import RobotComm	# yes dongle

class Event(object):
    def __init__(self, event_type, event_data):
        self.type = event_type #string
        self.data = event_data #list of number or character depending on type

##############################
# Finite state machine engine
##############################
class StateMachine(object):
	def __init__(self, name, eventQ_handle):
		self.name = name		# machine name
		self.states = []	# list of lists, [[state name, event, transition, next_state],...]
		self.start_state = None
		self.end_states = []	# list of name strings
		self.q = eventQ_handle
		return

	def set_start_state(self, state_name):
		self.start_state = state_name
		return

	def get_start_state(self):
		return self.start_state
		
	def add_end_state(self, state_name):
		self.end_states.append(state_name)
		return
			
	def add_state(self, state, event, callback, next_state):
		self.states.append([state, event, callback, next_state]) # append to list
		return
	
	# you must set start state before calling run()
	def run(self):
		current_state = self.start_state
		#while not self.q.empty(): # for a machine that has end states
		while True:
			#print "current state", current_state
			if current_state in self.end_states:
				break
			if not self.q.empty():
				e = self.q.get()
				for c in self.states:
					if c[0] == current_state and c[1] == e.type:
						#print('\nAction = %s, Transition = %s to %s' % (c[2], c[0], c[3]))
						#print('Transition = %s to %s' % (c[0], c[3]))
						c[2]()	# invoke callback function
						current_state = c[3] 	# next state
						break	# get out of inner for-loop
		return

################################
# Hamster control
################################
class RobotBehavior(object):
	def __init__(self):
		self.done = False	# set by GUI button
		self.go = False		# set by GUI button
		self.robot = None
		self.q = Queue.Queue()	# event queue for FSM
		self.spawn_threads()
		return

	def spawn_threads(self):
		###########################################################
		# 1. create a watcher thread that reads sensors and registers events: obstacle on left, right or no obstacle. This
		# 	thread runs the method event_watcher() you are to implement below.
		# 2. populate FSM(StateMachine) with avoidance states, set start state and create a thread to run the machine
		###########################################################	
		pass

	def event_watcher(self, q):
		just_turned_on = True

		while not self.done:
			if gRobotList and self.go:
				self.robot = gRobotList[0]
				if just_turned_on:
					#time.sleep(1)
					just_turned_on = False #the first time the robot connect, sensor data is unavailable the first second or so
				###########################################################
				# Implement event producer here. The events are obstacle on left, right or no obstacle. Design your
				# logic for what event gets created based on sensor readings.
				###########################################################
				time.sleep(0.01)
			# else:
			# 	print "waiting for robot in watcher"
	        return

	#######################################
	# Implement Hamster movements to avoid obstacle
	#######################################
	def turning_left(self):
		pass

	def turning_right(self):
		pass

	def moving_forward(self):
		pass
		  
class GUI(object):
	def __init__(self, root, robot_control):
		self.root = root
		self.robot_control = robot_control
		root.geometry('300x350')
		root.title('Hamster Control')

		canvas = tk.Canvas(root, bg="white", width=300, height=250)
		canvas.pack(expand=1, fill='both')
		canvas.create_rectangle(175, 175, 125, 125, fill="green")

		b1 = tk.Button(root, text='Go')
		b1.pack()
		b1.bind('<Button-1>', self.startProg)

		b2 = tk.Button(root, text='Exit')
		b2.pack()
		b2.bind('<Button-1>', self.stopProg)
		return
	
	def startProg(self, event=None):
		self.robot_control.go = True
		return

	def stopProg(self, event=None):
		self.robot_control.done = True		
		self.root.quit() 	# close window
		return

def main():
    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    global gRobotList
    gRobotList = comm.robotList

    behaviors = RobotBehavior()

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    return

if __name__ == "__main__":
    sys.exit(main())