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

def main():
    
    #input ("Enter the size of the  ")
    gridSize = [4, 4]

    obstacle = [2, 2]

    graph = {} #creates dictionary

    print gridSize[0]
    print type(gridSize[0])

    for i in range(gridSize[0]):
        for j in range (gridSize[1]):
            if ((i == obstacle[0] - 1) and (j == obstacle[1] - 1)):
                pass
            elif (i + 1 == obstacle[0] - 1):
                graph[str(i) + "," + str(j)] = set([str(i) + "," + str(j + 1)])
            elif (j + 1 == obstacle[1] - 1):
                graph[str(i) + "," + str(j)] = set([str(i + 1) + "," + str(j)])
            else:
                graph[str(i) + "," + str(j)] = set([str(i - 1) + "," + str(j), str(i + 1) + "," + str(j), str(i) + "," + str(j - 1), str(i) + "," + str(j + 1),])
 
    # graph = {'A': set(['B', 'C']),
    #      'B': set(['A', 'E', 'D']),
    #      'C': set(['A', 'F', 'G']),
    #      'D': set(['B', 'H']),
    #      'E': set(['B','I', 'J','L']),
    #      'F': set(['C','K', 'L']),
    #      'G': set(['C']),
    #      'H': set(['D']),
    #      'I': set(['E']),
    #      'J': set(['E']),
    #      'K': set(['F']),
    #      'L': set(['F', 'E'])}

    # nodes_location = [('A', [3,1]),
    #                 ('B', [2,2]),
    #                 ('C', [4,2]),
    #                 ('D', [1,3]),
    #                 ('E', [2,3]),
    #                 ('F', [4,3]),
    #                 ('G', [5,3]),
    #                 ('H', [1,4]),
    #                 ('I', [2,4]),
    #                 ('J', [3,4]),
    #                 ('K', [4,4]),
    #                 ('L', [5,4])]


    print 'graph:', graph

    frame = tk.Tk()
    frame.title('Simple Graph Display')
    frame.geometry("400x400")
    start_node = '0,0'
    end_node = '2,2'
    display = GraphDemo.SimpleGraphDisplay(frame, graph, start_node, end_node)

    bfs = bfsEngine.BFS(graph)
    p = bfs.bfs_shortest_path(start_node, end_node)
    display.highlight_path(p)
    frame.mainloop()
    return

if __name__ == main():
    sys.exit(main())
