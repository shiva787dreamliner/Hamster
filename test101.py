'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   PROPRIETARY and CONFIDENTIAL

   Creqted by Dr. Qin Chen
   7/2017
   ========================================================================*/
'''

import sys
sys.path.append('../')
import Tkinter as tk
from simple_graph import *
from tk_hamster_GUI_Sim import *

class MotionPlanner(object):
    def __init__(self, vWorld, start, goal):
        self.vWorld = vWorld
        self.start = start
        self.goal = goal
        return

    def worker(self):
        print'MotionPlanner is called'
        vWorld = self.vWorld
        start = self.start
        goal = self.goal
        canvas_width = vWorld.canvas_width
        canvas_height = vWorld.canvas_height
        cell_list = Queue.Queue()
        cell_list.put(vWorld.area)
        # inflate obstacles to form C-space
        self.compute_c_obstacles(vWorld,28)
        obs_list = vWorld.cobs
        vWorld.goal_list = []
        f_cell_list = []
        # Cut inflated obstacles out of C-space and divide workspace into cells from cutting 
        f_cell_list = self.compute_free_cells(cell_list, obs_list)
        # determine connectivity between free cells and locate the point to go from one cell to its neighbor
        point_list = self.compute_free_points(f_cell_list)
        
        raw_input('press RETURN to show free cells')
        for cell in f_cell_list:
            x1 = cell[0]
            y1 = cell[1]
            x2 = cell[2]
            y2 = cell[3]     
            vWorld.canvas.create_rectangle(canvas_width+x1, canvas_height-y1, canvas_width+x2, canvas_height-y2, outline = "black")
        
        raw_input('press RETURN to show start and goal')
        #create graph - nodes and edges for the point list
        myGraph = Graph()
        num_points = len(point_list)

        # creating nodes
        myGraph.add_node("s", start)
        myGraph.set_start("s")
        myGraph.add_node("g", goal)
        myGraph.set_goal("g")
        xs = start[0]
        ys = start[1]
        vWorld.canvas.create_oval(canvas_width+xs-6, canvas_height-ys-6, canvas_width+xs+6, canvas_height-ys+6, outline = "green", fill="green")
        xg = goal[0]
        yg = goal[1]
        vWorld.canvas.create_oval(canvas_width+xg-6, canvas_height-yg-6, canvas_width+xg+6, canvas_height-yg+6, outline = "purple", fill="purple")
        
        raw_input('press RETURN to show points connecting free cells, start, and goal')
        point_num = 1
        for point in point_list:
            myGraph.add_node(str(point_num), point)
            x1 = point[0]
            y1 = point[1]
            vWorld.canvas.create_oval(canvas_width+x1-4, canvas_height-y1-4, canvas_width+x1+4, canvas_height-y1+4, outline = "red")
            if self.connected(point, start, f_cell_list):
                g_cost = math.sqrt((xs-x1)*(xs-x1)+(ys-y1)*(ys-y1))
                print "creating edge: ", "s", str(point_num), g_cost
                myGraph.add_edge("s", str(point_num), g_cost)
                vWorld.canvas.create_line(canvas_width+x1, canvas_height-y1, canvas_width+xs, canvas_height-ys, fill="red")
            if self.connected(point, goal, f_cell_list):
                print "inside goal if"
                g_cost = math.sqrt((xg-x1)*(xg-x1)+(yg-y1)*(yg-y1))
                print "creating edge: ", "g", str(point_num), g_cost
                myGraph.add_edge("g", str(point_num), g_cost)
                vWorld.canvas.create_line(canvas_width+x1, canvas_height-y1, canvas_width+xg, canvas_height-yg, fill="red")
            point_num += 1

        raw_input("press RETURN to show connectivity")
        if num_points > 1:
            # creating edges
            #print "num points: ", num_points
            next_point = 2
            for i in range (1, num_points+1):
                #print "from: ", i
                point1 = point_list[i-1]
                x1 = point1[0]
                y1 = point1[1]
                for j in range (next_point, num_points+1):
                    #print "to: ", j
                    point2 = point_list[j-1]
                    x2 = point2[0]
                    y2 = point2[1]
                    if (self.connected(point1, point2, f_cell_list)):
                        g_cost = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
                        #print "creating edge: ", str(i), str(j), g_cost
                        myGraph.add_edge(str(i), str(j), g_cost)
                        vWorld.canvas.create_line(canvas_width+x1, canvas_height-y1, canvas_width+x2, canvas_height-y2, fill = "red")
                next_point += 1

        raw_input('press RETURN to show path')
        #print "search: ", myGraph.queue
        myGraph.Dijkstra()
        path = Queue.LifoQueue()
        if myGraph.nodes["g"].back_pointer:
            path.put(["pose", myGraph.nodes["g"].data[0], myGraph.nodes["g"].data[1], False])
            print "Found path"
            path_node = myGraph.nodes["g"].back_pointer
            while path_node.back_pointer != False:
                px = path_node.data[0]
                py = path_node.data[1]
                path.put(["pose", px, py, False])
                vWorld.canvas.create_oval(canvas_width+px-6, canvas_height-py-6, canvas_width+px+6, canvas_height-py+6, outline = "blue", fill="blue")
                path_node = path_node.back_pointer
            while not path.empty():
                vWorld.goal_list.append(path.get())
                vWorld.goal_list_index = 0
            print "path: ", vWorld.goal_list
        else:
            print "failed to find path"
        return

    def compute_c_obstacles(self, vworld, d): #d is the amount we need to expand by
        #print self.vWorld.map
        #cobs = []
        for obs in self.vWorld.map:
            cobs = []
            cobs.append(obs[0] - d)
            cobs.append(obs[1] - d)
            cobs.append(obs[2] + d)
            cobs.append(obs[3] + d)
            self.vWorld.cobs.append(cobs)   
        #print self.vWorld.cobs

    def compute_free_cells(self, cell_list, c_obs_list):
        xvalues = [] 
        border = cell_list.get() 
        f_cell_list = [] 
        
        xvalues.append(border[0])
        xvalues.append(border[2])

        for cobs in c_obs_list:
            if cobs[0] not in xvalues: 
                xvalues.append(cobs[0])
            if cobs[2] not in xvalues:
                xvalues.append(cobs[2])

        xvalues.sort(reverse = True)

        x2 = xvalues.pop()
        while xvalues:
            x1 = x2
            x2 = xvalues.pop()
            
            region = [x1, border[1], x2, border[3]]

            interObs = []


            for obs in c_obs_list:
                obsXmin = min(obs[0],obs[2])
                obsXmax = max(obs[0],obs[2])
                obsYmin = min(obs[1],obs[3])
                obsYmax = max(obs[1],obs[3])

                regionXmin = min(region[0], region[2])
                regionXmax = max(region[0], region[2])
                regionYmin = min(region[1], region[3])
                regionYmax = max(region[1], region[3])

                if ((obsXmin >= regionXmax or obsXmax <= regionXmin)) :
                    u = 1
                else:
                    interObs.append(obs)
            if interObs:
                print region
                dividedRegions = []
                yvalues = []
                yvalues.append(region[1])
                yvalues.append(region[3])
                for obs in interObs:
                    yvalues.append(obs[1])
                    yvalues.append(obs[3])
                yvalues.sort(reverse = True)
                y2 = yvalues.pop()
                while yvalues:
                    y1 = y2
                    y2 = yvalues.pop()
                    for obs in interObs:
                        obsXmin = min(obs[0],obs[2])
                        obsXmax = max(obs[0],obs[2])
                        obsYmin = min(obs[1],obs[3])
                        obsYmax = max(obs[1],obs[3])
                        if y1 != obsYmin:
                            newRegion = [regionXmin,y2,regionXmax,y1]
                            f_cell_list.append(newRegion)

                        if [regionXmin,obsYmax,regionXmax,obsYmin] in f_cell_list:
                            f_cell_list.remove([regionXmin,obsYmax,regionXmax,obsYmin])
            else:
                f_cell_list.append([x1, border[3], x2, border[1]])
        f_cell_list = list(map(list,set(map(tuple,f_cell_list))))
        return f_cell_list

    def two_cells_connected(self, cell1, cell2):
        # Given two free cells, cell1 and cell2.
        # return connecting point[x,y] if two cells are connected
        # return False if not connected
        print "inside twoCellConnected"
        leftCell = cell1
        rightCell = cell2
        yVals = []

        yVals.append(leftCell[1])
        yVals.append(leftCell[3])
        yVals.append(rightCell[1])
        yVals.append(rightCell[3])

        xPoint = 0
        yPoint = 0

        leftCellEdge = abs(leftCell[1] - leftCell[3])
        rightCellEdge = abs(rightCell[1] - rightCell[3])
        distance = rightCell[1] - leftCell[3]

        if (leftCell[2] == rightCell[0] and distance <= (leftCellEdge + rightCellEdge)):
            topRemain = abs(leftCell[1] - rightCell[1])
            #print "this is the top remainder", topRemain
            bottomRemain = abs(leftCell[3] - rightCell[3])
            #print "this is the bottom remainder", bottomRemain
            #totalLen = leftCellEdge + rightCellEdge
            #print "this is the totalLen", totalLen
            yMin = min(yVals)
            yMax = max(yVals)
            #print "min, max", yMin, yMax
            accountingForOverlap = abs(yMax - yMin)
            #print "this is accouting for the overlap", accountingForOverlap
            overlapLen = accountingForOverlap - (topRemain + bottomRemain)
            #print "this is the overlap length", overlapLen
            
            #print yVals
            for val in yVals:
                for anotherVal in yVals:
                    print "val, anotherVal", val, anotherVal
                    posOverlapLen = abs(val - anotherVal)
                    print "this is the posOverlapLen", posOverlapLen
                    if (posOverlapLen == overlapLen):
                        xPoint = leftCell[2]
                        yPoint = (val + anotherVal)/2.0
                        print xPoint
                        print yPoint
                        if (xPoint != self.vWorld.area[0] and xPoint != self.vWorld.area[2] and yPoint != self.vWorld.area[1] and yPoint != self.vWorld.area[3]):
                            return xPoint, yPoint
            return False
        else:
            print "returning false"
            return False

    def compute_free_points(self, f_cell_list):
        #MUST SORT REGIONS FROM LEAST TO GREATEST
        
        self.selectionSort(f_cell_list)
        print f_cell_list

        print "this is the f_cell_list", f_cell_list
        nodes = []
        # for freeCellIndex in range (len(f_cell_list)):
        #     if (freeCellIndex + 1 < len(f_cell_list)):
        #         #HAVE TO ADD IF FALSE (NOT CONNECTED
        #         nodes.append(self.two_cells_connected(f_cell_list[freeCellIndex], f_cell_list[freeCellIndex + 1]))

        for freeCell in f_cell_list:
            for anotherFree in f_cell_list:
                    nodes.append(self.two_cells_connected(freeCell, anotherFree))

        tempListForFalse = []
        for possNodeIndex in range(len(nodes)):
            print "this is a node in the for loop: ", nodes[possNodeIndex]
            if nodes[possNodeIndex] == False:
                tempListForFalse.append(possNodeIndex)

        counter = 0
        for index in tempListForFalse:
            index = index - counter 
            nodes.pop(index)
            counter = counter + 1

        print "this is the freee nodes", nodes
        return nodes

        # Obstacle free cells are given in f_cell_list
        # This function returns a list of points, each point is on overlapping edge of two conncted obstacle free cells.

    def connected(self, point1, point2, cell_list):
        for cell in cell_list:
            intersection1 = False
            intersection2 = False
            boolCheck = False
           
            cellXmin = min(cell[0],cell[2])
            cellXmax = max(cell[0],cell[2])
            cellYmin = min(cell[1],cell[3])
            cellYmax = max(cell[1],cell[3])

            if point1[0] <= cellXmax and point1[0] >= cellXmin and point1[1] <= cellYmax and point1[1] >= cellYmin:
                intersection1 = True
            if point2[0] <= cellXmax and point2[0] >= cellXmin and point2[1] <= cellYmax and point2[1] >= cellYmin:
                intersection2 = True
            if intersection1 and intersection2:
                return True
            else:
                boolCheck = True
        if (boolCheck == True):   
            return False

    def selectionSort(self, alist):
        for fillslot in range(len(alist)-1,0,-1):
           positionOfMax=0
           for location in range(1,fillslot+1):
               if alist[location]>alist[positionOfMax]:
                   positionOfMax = location

           temp = alist[fillslot]
           alist[fillslot] = alist[positionOfMax]
           alist[positionOfMax] = temp
        
class GUI(object):
    def __init__(self, gui_root, vWorld, endCommand):
        self.gui_root = gui_root
        gui_root.title("Motion Planner")
        self.endCommand = endCommand
        self.vWorld = vWorld
        self.start = [200, 0] # robot's start location, goal location is user defined
        self.initUI()
        return

    def initUI(self):
        #creating tje virtual appearance of the robot
        canvas_width = 440 # half width
        canvas_height = 300 # half height
        self.vWorld.canvas_width = canvas_width
        self.vWorld.canvas_height = canvas_height
        rCanvas  = tk.Canvas(self.gui_root, bg="light gray", width=canvas_width*2, height= canvas_height*2)
        self.vWorld.canvas = rCanvas
        rCanvas.pack()

        button0 = tk.Button(self.gui_root,text="Grid")
        button0.pack(side='left')
        button0.bind('<Button-1>', self.drawGrid)

        button1 = tk.Button(self.gui_root,text="Clear")
        button1.pack(side='left')
        button1.bind('<Button-1>', self.clearCanvas)

        button2 = tk.Button(self.gui_root,text="Map")
        button2.pack(side='left')
        button2.bind('<Button-1>', self.drawMap)

        button9 = tk.Button(self.gui_root,text="Exit")
        button9.pack(side='left')
        button9.bind('<Button-1>', self.endCommand)

        rCanvas.bind("<Button-1>", self.getGoal)
        return

    def drawGrid(self, event=None):
        print "draw Grid"
        canvas_width = self.vWorld.canvas_width
        canvas_height = self.vWorld.canvas_height
        rCanvas = self.vWorld.canvas
        x1 = 0
        x2 = canvas_width*2
        y1 = 0
        y2 = canvas_height*2
        del_x = 20
        del_y = 20
        num_x = x2 / del_x
        num_y = y2 / del_y
        # draw center (0,0)
        rCanvas.create_rectangle(canvas_width-3,canvas_height-3,canvas_width+3,canvas_height+3, fill="red")
        # horizontal grid
        for i in range (0,num_y):
            y = i * del_y
            rCanvas.create_line(x1, y, x2, y, fill="yellow")
        # verticle grid
        for j in range (0, num_x):
            x = j * del_x
            rCanvas.create_line(x, y1, x, y2, fill="yellow")
        return

    def drawMap(self, event=None):
        self.vWorld.draw_map()

    def clearCanvas(self, event=None):
        rCanvas = self.vWorld.canvas
        rCanvas.delete("all")
        return

    def getGoal(self, event):
        self.vWorld.canvas.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, outline = "blue")

        canvas_width = self.vWorld.canvas_width
        canvas_height = self.vWorld.canvas_height
        self.vWorld.goal_x = event.x - canvas_width
        self.vWorld.goal_y = canvas_height - event.y 
        print "selected goal: ",self.vWorld.goal_x, self.vWorld.goal_y
        s_point = self.start
        g_point = [self.vWorld.goal_x, self.vWorld.goal_y]
        print 'start pose(%s, %s): ' % (s_point[0], s_point[1])
        print 'goal pose(%s, %s): ' % (g_point[0], g_point[1]) 
        mp = MotionPlanner(self.vWorld, s_point, g_point)
        mp.worker()
        return

class VirtualWorld(object):
    def __init__(self, gui_root):
        self.gui_root = gui_root
        self.gui_handle = None
        self.vWorld = None
        self.create_world()
        return

    def create_world(self):
        self.vWorld = virtual_world()      
        #objects in the world
        self.vWorld.map = []

        #project 3-1
        #rect1 = [-50, 80, 50, 120]
        #rect2 = [100, -50, 140, 50]
        #rect3 = [-160, -50, -120, 50]
        #rect4 = [-50,-180, 50, -140]

        #project 3-2
        #rect1 = [-20, 80, 20, 120]
        #rect2 = [100, -20, 140, 20]
        #rect3 = [-20, -120, 20, -80]
        #rect4 = [-260,-30, -220, 30]
        #rect5 = [-220, -70, -180, -30]
        #rect6 = [-220, 30, -180, 70]

        #bounder of board
        rect1 = [-100, -180, 0, -140]
        rect2 = [-140, -180, -100, -80]
        rect3 = [-100, 140, 0, 180]
        rect4 = [-140, 80, -100, 180]
        rect5 = [0, -50, 40, 50]
        rect6 = [-260, -20, -220, 20]
        rect7 = [40, 60, 140, 100]
        #rect7 = [0, 0, 50, 50]

        # robot's work space boundary
        self.vWorld.area = [-308,-208,308,208]

        self.vWorld.add_obstacle(rect1)
        self.vWorld.add_obstacle(rect2)
        self.vWorld.add_obstacle(rect3)
        self.vWorld.add_obstacle(rect4)
        self.vWorld.add_obstacle(rect5)
        self.vWorld.add_obstacle(rect6)
        self.vWorld.add_obstacle(rect7)

        self.gui_handle = GUI(self.gui_root, self.vWorld, self.stopProg)
        return

    def stopProg(self, event=None):
        self.gui_root.quit()
        return

def main():
    m = tk.Tk() #root
    v_world = VirtualWorld(m)
    m.mainloop()
    return

if __name__== "__main__":
    sys.exit(main())
