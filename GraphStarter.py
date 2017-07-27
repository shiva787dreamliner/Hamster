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
    graph = {'A': set(['B', 'C']),
         'B': set(['A', 'E', 'D']),
         'C': set(['A', 'F', 'G']),
         'D': set(['B', 'H']),
         'E': set(['B','I', 'J']),
         'F': set(['C','K']),
         'G': set(['C']),
         'H': set(['D']),
         'I': set(['E']),
         'J': set(['E']),
         'K': set(['F'])}

    nodes_location = [('A', [3,1]),
                    ('B', [2,2]),
                    ('C', [4,2]),
                    ('D', [1,3]),
                    ('E', [2,3]),
                    ('F', [4,3]),
                    ('G', [5,3]),
                    ('H', [1,4]),
                    ('I', [2,4]),
                    ('J', [3,4]),
                    ('K', [4,4])]
     
    
    print 'graph:', graph

    frame = tk.Tk()
    frame.title('Simple Graph Display')
    frame.geometry("400x400")
    start_node = 'A'
    end_node = 'J'
    display = GraphDemo.SimpleGraphDisplay(frame, graph, nodes_location, start_node, end_node)

    bfs = bfsEngine.BFS(graph)
    p = bfs.bfs_shortest_path(start_node, end_node)
    display.highlight_path(p)
    frame.mainloop()
    return

if __name__ == main():
    sys.exit(main())
