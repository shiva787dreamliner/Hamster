'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          tk_simple_graph_starter.py
   By:            Qin Chen
   Last Updated:  6/10/17

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''

import sys
import Tkinter as tk
import bfsEngine
import GraphDemo
import RobotBehavior
import time
import threading
from HamsterAPI.comm_ble import RobotComm

gRobotList = []

def mainForGraphFSM(gridSizeIn, obsIn, frameIn): 
    gridSize = gridSizeIn
    obs = obsIn
    frame = frameIn
    #print type(gridSize)
    #gridSize = [4, 4]
    #print gridSize[0]
    #print gridSize[1]


    #print obs
    
    #obs = "1,2"

    graph = {} #creates dictionary

    for i in range(gridSize[0]):
        for j in range (gridSize[1]):
            for obstacle in obs:
                if (i == int(obstacle[0]) and j == int(obstacle[1])):
                    #print "entering removal of stuff statement"
                    break
            else:
                graph[str(i) + "," + str(j)] = set([str(i - 1) + "," + str(j), str(i + 1) + "," + str(j), str(i) + "," + str(j - 1), str(i) + "," + str(j + 1),])
                
                if (i == 0):
                    graph[str(i) + "," + str(j)].remove(str(i - 1) + "," + str(j)) 
                if (i == gridSize[0] - 1):
                    graph[str(i) + "," + str(j)].remove(str(i + 1) + "," + str(j)) 
                if (j == 0):
                    graph[str(i) + "," + str(j)].remove(str(i) + "," + str(j - 1)) 
                if (j == gridSize[1] - 1):
                    graph[str(i) + "," + str(j)].remove(str(i) + "," + str(j + 1)) 
            
    for obstacle in obs:
        for node in graph:
            ##print graph[node]
            for connections in graph[node]:
                if (obstacle[0] == int(connections[0]) and obstacle[1] == int(connections[2])):
                    graph[node].remove(connections)
                    break

    #print 'graph:', graph

    start_node = '3,3'
    end_node = '1,1'
    display = GraphDemo.SimpleGraphDisplay(frame, graph, start_node, end_node)

    bfs = bfsEngine.BFS(graph)
    p = bfs.bfs_shortest_path(start_node, end_node)
    print "shortest path", p
    display.highlight_path(p)

    #print gRobotList
    fsm = RobotBehavior.finiteStateMachine(p, graph, start_node, end_node, gRobotList, display, bfs)
    fsm.executingFSM()
    #print "SHABALABADINGDONG"

def main(): 

    robotComm = RobotComm(1)
    commCheck = False

    global gRobotList
    robotComm.start() #starts comm thread 
    #print "Bluetooth connected"
    gRobotList = robotComm.robotList

    frame = tk.Tk()
    frame.title('Simple Graph Display') #?!?!?!?!??!?!
    frame.geometry("400x400")

    gridSize = input("Enter the size of the grid as length by width dimensions: ")
    obs = []
    noObs = False

    while not noObs:
        obsIn = input("Enter the location of obstacle in a coordinate fromat. Enter done if you are done putting in obstacles: ")
        # #print str(obsIn)
        # #print type(str(obsIn))
        if obsIn == "done":
            noObs = True
        else:
            obs.append(obsIn)

    #print "before init thread"
    threadForGraphFsM = threading.Thread(target = mainForGraphFSM, args = (gridSize, obs, frame))
    threadForGraphFsM.start()
    #print "thread started"

    frame.mainloop() 

    robotComm.stop()
    robotComm.join()
    return


if __name__ == main():
    sys.exit(main())
