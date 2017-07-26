import sys
import time
import threading
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm
#add import statement for abstract class

gRobotList = []
gQuit = False
#flag it as global here?
def main(): 
	robotComm = RobotComm(1)
	commCheck = False

	global gRobotList
	robotComm.start() #starts comm thread 
	print "Bluetooth connected"
	gRobotList = robotComm.robotList

	frame = tk.Tk()
	frame.mainloop()

	print "terimanted"

if __name__ == "__main__":
	main()