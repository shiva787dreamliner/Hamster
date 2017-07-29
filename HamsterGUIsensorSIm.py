'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:            Qin Chen
   Last Updated:  4/10/17

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import threading
import Tkinter as tk
import time  # sleep
from HamsterAPI.comm_ble import RobotComm
#for PC, need to import from commm_usb

gQuit = False

class SensorDisplayThread(threading.Thread):
    def __init__(self, canvas, robotList):
        super(SensorDisplayThread, self).__init__()
        self.robotList = robotList
        self.canvas = canvas

        ###########################################################
        # Display a blue rectangle in center of window, representing Hamster.
        # Create a line segment for left proximilty sensor display
        # Create a line segment for right proxijity sensor display
        # Creat a rectangle for displaying the left floor sensor 
        # Create a rectangle for displaying the right floor sensor
        ###########################################################
        self.hamster = (125, 125, 175, 175)
        self.hamsterID = self.canvas.create_rectangle(self.hamster, fill = "blue")
        self.floorRect = (130, 130, 145, 140)
        self.floorRectID = self.canvas.create_rectangle(self.floorRect, fill = "white")
        self.floorRect2 = (155, 130, 170, 140)
        self.floorRectID2 = self.canvas.create_rectangle(self.floorRect2, fill = "white")
        self.lProx = (130, 120, 130, 110)
        self.lProxID = self.canvas.create_line(self.lProx, fill = "red")
        self.rProx = (170, 120, 170, 110)
        self.rProxID = self.canvas.create_line(self.rProx, fill = "red")

        #hamsterID.pack()

        return

    def run(self):   
        while not gQuit:
            if self.robotList:
                for robot in self.robotList:
                    ##############################
                    # Your code for displaying proximity sensors
                    ##############################
                    #print "display prox sensors here"
                    lProx = robot.get_proximity(0)
                    rProx = robot.get_proximity(1)

                    if (lProx > 0 and rProx > 0):
                        lDistance = 1000*(1.0/lProx) #0.25*(1/lProx)
                        rDistance = 1000*(1.0/rProx) #0.25*(1/lProx)
                        print "prox left", lDistance
                        print "prox right", rDistance

                        self.canvas.coords(self.lProxID, 130, 120, 130, (110 - lDistance))
                        self.canvas.coords(self.rProxID, 170, 120, 170, (110 - rDistance))


                    ################################
                    # Your code for displaying floor sensors
                    if (robot.get_floor(0) > 50):
                        self.canvas.itemconfig(self.floorRectID, fill = "white")
                    else:
                        self.canvas.itemconfig(self.floorRectID, fill = "black")
                    if (robot.get_floor(1) > 50):
                        self.canvas.itemconfig(self.floorRectID2, fill = "white")
                    else:
                        self.canvas.itemconfig(self.floorRectID2, fill = "black")
                    ################################
                    print "display floor sensors here"
            else:
                print "waiting for robot"
            time.sleep(0.1)

        for robot in self.robotList:
            robot.reset()
        return

class RobotMoves(object):
    def __init__(self, robotList):
        self.robotList = robotList
        return

    def move_up(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,100)
                robot.set_wheel(1,100)
        else:
            print "waiting for robot"

    def move_down(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, -100)
                robot.set_wheel(1, -100)
            else:
                print "waiting for robot" 


    def move_left(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, -100)
                robot.set_wheel(1, 100)
            else:
                print "waiting for robot"

    def move_right(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, 100)
                robot.set_wheel(1, -100)
            else:
                print "waiting for robot"


    def stop_move(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, 0)
                robot.set_wheel(1, 0)
            else:
                print "waiting for robot"


class UI(object):
    def __init__(self, root, robot_moves):
        self.root = root
        self.robot_moves = robot_moves  # handle to robot commands
        self.canvas = None
        self.initUI()
        return

    def initUI(self):
        ###################################################################
        # Create a Hamster joystick window which contains
        # 1. a canvas where "sensor readings" are displayed
        # 2. a button for exit, i.e., a call to stopProg(), given in this class
        # 3. listen to key press and key release when focus is on this window
        ###################################################################
        self.canvas = tk.Canvas(self.root, bg = "white", width = 300, height = 300)
        self.canvas.pack()
        exitButton = tk.Button(self.root, text = "Exit", command = self.stopProg)

        #You don't bind keys to graphics
        self.root.bind("<KeyPress>", self.keydown)
        self.root.bind("<KeyRelease>", self.keyup)
    
    ####################################################
    # Implement callback function when key press is detected
    ####################################################
    def keydown(self, event):
        if event.char == 'w':
            self.robot_moves.move_up(event)
        if event.char == 'a':
            self.robot_moves.move_left(event)
        if event.char == 's':
            self.robot_moves.move_down(event)
        if event.char == 'd':
            self.robot_moves.move_right(event)

    #####################################################
    # Implement callback function when key release is detected
    #####################################################
    def keyup(self, event):
        self.robot_moves.stop_move()

    def stopProg(self, event=None):
        global gQuit
        gQuit = True
        self.root.quit()    # close window
        return

def main(argv=None):
    gMaxRobotNum = 1; # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    robot_moves = RobotMoves(robotList)
    m = tk.Tk() #root
    gui = UI(m, robot_moves)
    global gQuit
    gQuit = False
    # start a watcher thread
    display=SensorDisplayThread(gui.canvas, robotList)
    display.setDaemon(True)
    display.start()
    
    m.mainloop()

    comm.stop()
    comm.join()

if __name__== "__main__":
    sys.exit(main())