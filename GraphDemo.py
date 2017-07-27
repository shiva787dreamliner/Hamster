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
    def __init__(self, frame, graph, nodes_location, start_node=None, goal_node=None):
        self.node_dist = 60
        self.node_size = 20
        self.gui_root = frame
        self.canvas = None
        self.graph = graph
        self.nodes_location = nodes_location
        self.start_node = start_node
        self.goal_node = goal_node
        self.display_graph()
        return

    def display_graph(self):        
        self.canvas = tk.Canvas(self.gui_root, bg="white", width=300, height=300)
        self.canvas.pack(expand=1, fill='both')
        for node in self.nodes_location:
            print 'node in display graph', node
            if node[0] == self.start_node:
                self.draw_node(node, 'red')
            elif node[0] == self.goal_node:
                self.draw_node(node, 'green')
            else:
                self.draw_node(node, 'blue')
            #pdb.set_trace()
            # get list of names of connected nodes
            connected_nodes = self.graph[node[0]]
            # find location for each connected node and draw edge
            if connected_nodes:
                for connected_node in connected_nodes:
                    # step into node locations list
                    for a_node in self.nodes_location:
                        if connected_node == a_node[0]:
                            self.draw_edge(node, a_node,'blue')

        return

    def highlight_path(self, path):
        for node_name in path:
            if (node_name != self.start_node) and (node_name != self.goal_node):          
                for a_node in self.nodes_location:
                    if node_name == a_node[0]:
                        print 'node in highlight path', a_node
                        self.draw_node(a_node, 'orange')
        return
  
    def draw_node(self, node, n_color):
        node_name = node[0]
        x = node[1][0]
        y = node[1][1]
    
        dist = self.node_dist
        size = self.node_size
        self.canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
        self.canvas.create_text(x*dist, y*dist,fill="white",text=node[0])
        return

    def draw_edge(self, node1, node2, e_color):
        x1 = node1[1][0]
        y1 = node1[1][1]
        x2 = node2[1][0]
        y2 = node2[1][1]
        dist = self.node_dist
        self.canvas.create_line(x1*dist, y1*dist, x2*dist, y2*dist, fill=e_color)
        return
          
