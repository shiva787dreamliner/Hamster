'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   This is a program that is provided to students in Robot AI class.
   Students use this it to build different Hamster behaviors.

   Name:          starter1.py
   By:            Qin Chen
   Last Updated:  6/10/16

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm	# no dongle
#from HamsterAPI.comm_usb import RobotComm	# yes dongle

################################
# Hamster control
################################
class RobotBehaviorThread(threading.Thread):
	def __init__(self):
		super(RobotBehaviorThread, self).__init__()
		self.done = False
		self.square = False
		self.shy = False
		self.follow = False
		self.dance = False
		self.pause = False
		return

	def run(self):
		robot=None
		while not self.done:
			if gRobotList:
				robot = gRobotList[0]	# max 1 robot per student
			if (self.pause == True):
				robot.set_wheel(0, 0)
				robot.set_wheel(1, 0)

			if robot and not self.pause:
				
				prox_l = robot.get_proximity(0)
				prox_r = robot.get_proximity(1)

				if (self.square == True):
					print "working!"
					robot = gRobotList[0]
					robot.set_wheel(1, 30)
					robot.set_wheel(0, 30)
					time.sleep(1)
					robot.set_wheel(1, -30)
					robot.set_wheel(0, 30) 
					time.sleep(1)

				elif (self.shy == True):
					if (prox_l != 0 or prox_r != 0):
						robot.set_wheel(0, -(prox_l*3))
						robot.set_wheel(1, -(prox_r*3))
					else:
						robot.set_wheel(0, 0)
						robot.set_wheel(1, 0)

				elif (self.follow == True):
					if (prox_l < 50 or prox_r < 50):
						robot.set_wheel(0, (50 - prox_l) * 2)
						robot.set_wheel(1, (50 - prox_r) * 2)

				elif (self.dance == True):
					if (prox_l < 50 or prox_r < 50):
						robot.set_wheel(0, 50)
						robot.set_wheel(1, 50)
					elif (prox_l >= 40 or prox_r >= 40):
						robot.set_wheel(0, -50)
						robot.set_wheel(1, -50)
					else:
						robot.set_wheel(0, 0)
						robot.set_wheel(1, 0)
					
					print "prox l/r", prox_l, prox_r

					#############################################
					# END OF YOUR WORKING AREA!!!
					#############################################					
		# stop robot activities, such as motion, LEDs and sound
		# clean up after exit button pressed
			#robot.set_wheel(0, 0)
			#robot.set_wheel(1, 0)
		if robot:
			robot.reset()
			time.sleep(0.1)
		return

	



class GUI(object):
	def __init__(self, root, robot_control):
		self.root = root
		self.robot_control = robot_control
		root.geometry('250x30')
		root.title('Hamster Control')

		b3 = tk.Button(root, text='Square')
		b3.pack(side='left')
		b3.bind('<Button-1>', self.square)

		b4 = tk.Button(root, text='Follow')
		b4.pack(side='left')
		b4.bind('<Button-1>', self.follow)

		b5 = tk.Button(root, text='Shy')
		b5.pack(side='left')
		b5.bind('<Button-1>', self.shy)

		b6 = tk.Button(root, text='Dance')
		b6.pack(side='left')
		b6.bind('<Button-1>', self.dance)

		b7 = tk.Button(root, text='Pause')
		b7.pack(side='left')
		b7.bind('<Button-1>', self.pause)

		b2 = tk.Button(root, text='Exit')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.stopProg)

		return

	def stopProg(self, event=None):
		self.robot_control.done = True		
		self.root.quit() 	# close window
		return

	def square(self, event=None):
		self.robot_control.go = False
		self.robot_control.done = False
		self.robot_control.shy = False
		self.robot_control.follow = False
		self.robot_control.dance = False
		self.robot_control.pause = False

		self.robot_control.square = True		
		return

	def follow(self, event=None):
		self.robot_control.go = False
		self.robot_control.done = False
		self.robot_control.shy = False
		self.robot_control.dance = False
		self.robot_control.square = False
		self.robot_control.pause = False	

		self.robot_control.follow = True
		return

	def dance(self, event=None):
		self.robot_control.go = False
		self.robot_control.done = False
		self.robot_control.shy = False
		self.robot_control.follow = False
		self.robot_control.square = False
		self.robot_control.pause = False	

		self.robot_control.dance = True
		return

	def shy(self, event=None):
		self.robot_control.go = False
		self.robot_control.done = False
		self.robot_control.follow = False
		self.robot_control.dance = False
		self.robot_control.square = False
		self.robot_control.pause = False

		self.robot_control.shy = True
		return

	def pause(self, event=None):
		self.robot_control.pause = True
		return



#################################
# Don't change any code below!! #
#################################

def main():
    # instantiate COMM object
    global gRobotList

    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'  
    gRobotList = comm.robotList

    behaviors = RobotBehaviorThread()
    behaviors.start()

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())

