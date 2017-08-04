import sys
import time
import threading
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm

gRobotList = []
gQuit = False

def main(): 
	robotComm = RobotComm(1)
	commCheck = False

	global gRobotList
	robotComm.start() #starts comm thread 
	print "Bluetooth connected"
	gRobotList = robotComm.robotList

	frame = tk.Tk()
	frame.title('C-Space Display') #?!?!?!?!??!?!
    frame.geometry("400x400")

    obs = []
    noObs = False

    while not noObs:
        obsIn = input("Enter the location of obstacle in a coordinate fromat. Enter done if you are done putting in obstacles: ")
        #print str(obsIn)
        #print type(str(obsIn))
        if obsIn == "done":
            noObs = True
        else:
            obs.append(obsIn)

	frame.mainloop()

	print "terimanted"

if __name__ == "__main__":
	main()