'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          tk_simple_graph_display.py
   By:            Qin Chen
   Last Updated:  6/10/17

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''

import sys
import pdb
import Tkinter as tk

##############
# Data types used in this implementation: dictionary, set, list.
# A simple graph is one with no edge cost or direction.
# SimpleGraphDisplay takes SimpleGraph as its input. 
#
##############

class SimpleGraphDisplay(object):
    def __init__(self, frame, graph, start_node=None, goal_node=None):
        self.node_dist = 60
        self.node_size = 20
        self.gui_root = frame
        self.canvas = None
        self.graph = graph
        self.start_node = start_node
        self.goal_node = goal_node
        self.canvas = tk.Canvas(self.gui_root, bg="white", width=300, height=300)
        self.canvas.pack(expand=1, fill='both')
        self.display_graph()
        return

    def updateGraph(self, newObs, removedObs):
        #print "in update graph method"
        removedNodes = []
        for obs in newObs:
            for nodeName in self.graph:
                if nodeName == obs:
                    removedNodes.append(nodeName)

        for node in removedNodes:
            self.graph.pop(node)

        #print ('hello, from line 46')
        for obstacle in newObs:
            for node in self.graph:
                ##print "in inner loop"
                ##print graph[node]
                for connections in self.graph[node]:
                    if (obstacle == connections):
                        #print "removing connections"
                        self.graph[node].remove(connections)
                        break
        #print self.graph
        self.canvas.delete("all")
        self.display_graph()
        return self.graph
        

    def convertToCoord(self, nodeKey): 

        index = 0
        for i in range (len(nodeKey)):
            if nodeKey[i] == ",":
                index = i 
                ##print index

        x = int(nodeKey[:index]) + 1
        y = int(nodeKey[index+1:]) + 1
        
        return x, y

    def display_graph(self):        
        #iterating through a dict essentially iterating through the jey
        #print "this is the graph in display graph", self.graph
        for nodeKey in self.graph:
            ##print 'node in display graph', node, type(node)
            if nodeKey == self.start_node:
                self.draw_node(nodeKey, 'red')
            elif nodeKey == self.goal_node:
                self.draw_node(nodeKey, 'green')
            else:
                self.draw_node(nodeKey, 'blue')
            #pdb.set_trace()
            # get list of names of connected nodes
            connected_nodes = self.graph[nodeKey]
            # find location for each connected node and draw edge
            if connected_nodes:
                for connected_node in connected_nodes:
                    # step into node locations list
                    for otherKey in self.graph:
                        if connected_node == otherKey:
                            self.draw_edge(nodeKey, otherKey,'blue')

        return

    def highlight_path(self, path):
        #print "this is the path", path
        pastNodeName = self.start_node
        pastNodeKey = None
        for node_name in path:
            if node_name == self.goal_node:
                for endNodeKey in self.graph:
                        if endNodeKey == pastNodeName:
                            pastNodeKey = endNodeKey
                        if endNodeKey == node_name:
                            currentNodeKey = endNodeKey
                            self.draw_edge(pastNodeKey, currentNodeKey, 'orange')
            if (node_name != self.start_node) and (node_name != self.goal_node):          
                for aNodeKey in self.graph:
                    if node_name == aNodeKey:
                        ##print 'node in highlight path', a_node
                        self.draw_node(aNodeKey, 'orange')
                    currentNodeName = node_name
                    for pathNodeKey in self.graph:
                        if pathNodeKey == currentNodeName:
                            currentNodeKey = pathNodeKey
                        if pathNodeKey == pastNodeName:
                            pastNodeKey = pathNodeKey
                    #print pastNodeKey
                    self.draw_edge(pastNodeKey, currentNodeKey, 'orange')
                    pastNodeName = currentNodeName


        return
  
    def draw_node(self, nodeKey, n_color):
        #node is a dictionary of strings to sets
        node_name = nodeKey
        
        x, y = self.convertToCoord(nodeKey)

        #print "coordinates", x,y
    
        dist = self.node_dist
        size = self.node_size
        self.canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
        self.canvas.create_text(x*dist, y*dist,fill="white",text=nodeKey)
        return

    def draw_edge(self, nodeKey1, nodeKey2, e_color):
        # x1 = node1[1][0]
        # y1 = node1[1][1]
        x1, y1 = self.convertToCoord(nodeKey1)
        x2, y2 = self.convertToCoord(nodeKey2)
        # x2 = node2[1][0]
        # y2 = node2[1][1]
        dist = self.node_dist
        self.canvas.create_line(x1*dist, y1*dist, x2*dist, y2*dist, fill=e_color)
        return
          
