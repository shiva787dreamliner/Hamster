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
'''class PIDControl:
	def_init_(self):
		self.error = '''


class RobotBehaviorThread(threading.Thread):
	def __init__(self):
		super(RobotBehaviorThread, self).__init__()
		self.done = False
		self.lineFollow = False
		self.pause = False
		return

	def proportion(self, robot):
		floorL = robot.get_floor(0)
		floorR = robot.get_floor(1)

		print "floor l/r", floorL, floorR

		leftError = 100 - floorL
		rightError = 100 - floorR

		if (leftError <= 5 and rightError <= 5):
			robot.set_wheel(1, 20)
			robot.set_wheel(0, 20)
		else:
			robot.set_wheel(1, int(leftError * 2))
			robot.set_wheel(0, int(rightError* 2))

	def run(self):
		print "in run"
		robot=None
		while not self.done:
			if gRobotList:
				robot = gRobotList[0]	# max 1 robot per student
			if (self.pause == True):
				robot.set_wheel(0, 0)
				robot.set_wheel(1, 0)
				break
			
			if robot and self.lineFollow:
				
				'''floorL = robot.get_floor(0)
				floorR = robot.get_floor(1)

				leftError = 100 - floorL
				rightError = 100 - floorR'''

				self.proportion(robot)

				'''errorPID = []
				errorPID.add(floorR - floorL)'''


				'''if (floorL == floorR):
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)

				elif (floorL < floorR):
					robot.set_wheel(1, floorR)
					robot.set_wheel(0, floorL)

				elif (floorR < floorL):
					robot.set_wheel(0, floorL)
					robot.set_wheel(1, floorR)'''

					
				

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
		root.geometry('250x70')
		root.title('Hamster Control')

		b1 = tk.Button(root, text='Line Follow')
		b1.pack(side='left')
		b1.bind('<Button-1>', self.lineFollow)

		b7 = tk.Button(root, text='Pause')
		b7.pack(side='left')
		b7.bind('<Button-1>', self.pause)

		b2 = tk.Button(root, text='Exit')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.stopProg)

		return

	def lineFollow(self, event=None):
		print "working"
		self.robot_control.lineFollow = True	
		self.robot_control.pause = False
		return

	def stopProg(self, event=None):
		self.robot_control.done = True		
		self.root.quit() 	# close window
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

