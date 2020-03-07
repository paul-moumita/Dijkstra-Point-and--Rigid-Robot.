import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import math
from collections import deque, namedtuple
from collections import defaultdict
from heapq import *
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon
import time
from ExplorePoint import ToExplore

'''
##--------------------------------------------------------------------------------------##
## We are defining Variables here: -
##--------------------------------------------------------------------------------------##
'''

start = []
end = []
resolution = 0
radius = 0
clearance = 0



title = 'Click to initialize co-ordinates'
window = tk.Tk()



##Now we will assign a default distance to the nodes we have in the frame##

inf = float('inf')

'''
##--------------------------------------------------------------------------------------##
##Functions will be defined here##
##--------------------------------------------------------------------------------------##
'''


'''
##To pick the coordinates from the window created in tkinter, we are creating a function 
##called OnClickFetch which will fetch the x and y coordinates for start and end points
'''

Border = namedtuple('Border', 'start, end, cost')

def makeborder(start, end, cost=1):
    return Border(start, end, cost)

def test(algo_type):
    pass


def sorting(vals):
    print(vals)
    return vals


def getKey(item):
    return item[0]


def OnClick(event):
    print(event.xdata, event.ydata)
    global start, end, title
    
    if (not (start)):
        start = [int(event.xdata), int(event.ydata)]
        print('selected start point co-ordinates are:')
        print(event.xdata, event.ydata)
    else:
        end = [int(event.xdata), int(event.ydata)]
        print('selected end point co-oridnates are:')
        print(event.xdata, event.ydata)
    return True


'''

To visualize the map for fetching data, we will create canvas with specifications here:
we will be giving the list with obstacle specifications here

'''

def create_Initial(ObList):
    global start, end, title, window

    figure = plt.Figure(figsize = (10,7)) #the figure will be plotted in 10inches by 7inches area on screen
    mark = figure.add_subplot(111) #the grid for plotting the map on canvas
    bgcanvas = FigureCanvasTkAgg(figure, window) #to draw the canvas and call matplotlib in tk
    bgcanvas.get_tk_widget().pack(fill=tk.NONE, expand = False) #fill is on default - so that the actual matplot won't expand even if the canvas is expanded

    #Plot a overall map in cream colour
    mark.fill([300, 0, 0, 300], [200, 200, 0, 0], color=(1, 0.96, 0.88))

    #logic to fill the obstacles to be created on the map
    for element in (ObList):
        mark.fill(element[0], element[1], color = element[2])

    #labelling elements of map    
    mark.set_title(title);
    mark.set_xlabel('X axis')
    mark.set_ylabel('Y axis')

    #To get co-ordinates on click using function: OnClick
    figure.canvas.mpl_connect('mouseclick_event_in_frame', OnClick)

    # for start point co-ordinates: -    
    tk.Label(window, text="Enter Coordinates").pack()
    tk.Label(window, text="Initial point(comma separated x,y-no spaces)").pack()

    
    Initial_Value = Entry(window)
    if (start):
        initial_str = str(start[0]) + ' ' + str(start[1])
        Initial_Value.insert(0, initial_str)
    Initial_Value.pack()

     # for end point co-ordinates: -  
    tk.Label(window, text="Final point(comma separated x,y-no spaces)").pack()
    Endpoint_Value = Entry(window)

    
    if (end):
        final_str = str(end[0]) + ' ' + str(end[1])
        Endpoint_Value.insert(0, final_str)
    Endpoint_Value.pack()

    # to initiate the processing to find the shirtest path
    tk.Button(window, text="Start Processing", command=lambda: process(Initial_Value, Endpoint_Value)).pack()

    window.mainloop()
    return ObList



'''
final animation

'''



def create_Final(i, nodes, node, test):
    if (i):
        if (((nodes[0].x) == i.x) and (nodes[0].y == i.y)):
            mark.scatter(int(i.x), int(i.y), s=5, c='g')
        else:
            mark.scatter(int(i.x), int(i.y), s=5, c='c')

        if (((nodes[len(nodes) - 1].x) == i.x) and (nodes[len(nodes) - 1].y == i.y)):
            node.PrintPath(mark)


            

'''

This function is to exit the map and start the processing with data
obtained from the user end

'''


def process(Initial_Value, Endpoint_Value):
    global window, start, end, radius, resolution, clearance
    resolution = 1
    if (Initial_Value.get()):
        x, y = (Initial_Value.get()).split(',')
        start = [int(int(x) / resolution), int(int(y) / resolution)]
    elif (start):

        start = [int(start[0] / resolution), int(start[1] / resolution)]
        print('start point', start)

    if (Endpoint_Value.get()):
        x1, y1 = (Endpoint_Value.get()).split(',')
        end = [int(int(x1) / resolution), int(int(y1) / resolution)]
    elif (end):
        end = [int(end[0] / resolution), int(end[1] / resolution)]
        print('End point', end)
    radius = 0
    clearance = 0
    window.quit()
    window.destroy()


'''

This function is to create the blueprint for dynamics of the robot direction -
mathematical equations

Basically, this function will be called by the dijsktra function to simulate the directions and generate pointers for all kind of nodes that we need.

'''




def map_math(weightx, weighty, cost, end, graph, default_listdict,
             Mod_internal_Allocations, parent, visited_nodes, next_node, pol):
    flag = 0
    mmapx = parent.x
    mmapy = parent.y
    global radius, clearance, resolution

    min_value_x = min(end[0], start[0]) - 1
    min_value_y = min(end[1], start[1]) - 1
    max_value_x = max(end[0], start[0]) + 1
    max_value_y = max(end[1], start[1]) + 1


    for i in range(8):

        x = mmapx + weightx[i]
        y = mmapy + weighty[i]

        cost_var = cost[i]
        parent_var = str(mmapx) + ' ' + str(mmapy)
        node_var = str(x) + ' ' + str(y)
        con_1= (parent_var, node_var, cost_var)
        con_2 = (node_var, parent_var, cost_var)

        if ((con_1 not in graph) and (con_2 not in graph) and (
                x >= 0 and x <= ((300 / resolution) + radius) and y >= 0 and y <= ((200 / resolution) + radius))):

            minmax = [min_value_x, min_value_y, max_value_x, max_value_y]
            if ((pathAvailability(x, y, minmax, pol) == 1) and (x >= (min_value_x) and y >= (min_value_y)) and (x <= (max_value_x) and y <= (max_value_y))):

                graph.append(con_1)
                test.append((x, y))
                if (node_var not in visited_nodes):
                    visited_nodes.add(node_var)

                    next = (cost_var + parent.cost)
                    var_to_explore = (ToExplore(node_var, (next), x, y))
                    var_to_explore.parent = parent
                    next_node[node_var] = next
                    Mod_internal_Allocations.append((next, var_to_explore))
                else:
                    required = [var for i, var in (Mod_internal_Allocations) if var.node == node_var]
                    prev = level_a.get(Mod_internal_Allocations, None)
                    next = (cost_var + parent.cost)
                    if prev is None or next < prev:
                        required[0].parent = parent
                        next_node[Mod_internal_Allocations] = next

                        required[0].cost = next
            else:
                min_value_x = minmax[0]
                min_value_y = minmax[1]
                max_value_x = minmax[2]
                max_value_y = minmax[3]



'''

path availibility

'''

def ObDefined(x, y, minmax, pol):
    
    global radius, clearance, resolution
    
    dnd = radius + clearance
    if (((y - ((76 / resolution) + dnd)) <= 0) and ((x - ((100 / resolution) + dnd)) <= 0) and ((-y + ((30 / resolution) - dnd)) <= 0) and ((-x + ((30 / resolution) - dnd)) <= 0)):
        updateboundaries(x, y, minmax)
        return 0
    rec = Point(x, y)


    if (((y - ((40 / resolution) + dnd)) <= 0) and ((x - ((250 / resolution) + dnd)) <= 0) and ((-y + ((10 / resolution) - dnd)) <= 0) and ((-x + ((200 / resolution) - dnd)) <= 0)):
        updateboundaries(x, y, minmax)
        return 0
    kite = Point(x, y)

    for i in pol:
        coords = i
        poly = Polygon(i)
        inside1 = rec.within(poly)
        inside2 = kite.within(poly)
        if (inside1 == True):
            break
        elif (inside2 == True):
            break
        
    if (inside1 == True or inside2 == True ):
        print(x, y, 'in poly')
        updateboundaries(x, y, minmax)
        return 0
    if ((((math.pow((x - (150 / resolution)), 2) / math.pow(((40 / resolution) + dnd), 2)) + (math.pow((y - (100 / resolution)), 2) / math.pow(((20 / resolution) + dnd), 2)) - 1) <= 0)):
        updateboundaries(x, y, minmax)
        # print(x,y,'in ellipse')
        return 0
    if ((((math.pow((x - (225 / resolution)), 2)) + (math.pow((y - (150 / resolution)), 2)) - (math.pow(((25 / resolution) + dnd), 2))) <= 0)):
        updateboundaries(x, y, minmax)
        # print(x,y,'in circle')
        return 0

    else:

        return 1


def dijkstra(graph, initial_str, final_str, paths_to_goal, mmapx, mmapy, weightx, weighty, costw, end, pol):
        path = []
        paths_to_goal = []

        count = -1
        path = 0
        queue = []
        queue.append((mmapx, mmapy))
        default_listdict = defaultdict(list)

        Mod_internal_Allocations, visited_node, next_node = [(0, Node(initial_str, 0, mmapx, mmapy))], set(), {initial_str: 0}
        nodes = []

        count = 0
        while Mod_internal_Allocations:
            (cost, parent) = Mod_internal_Allocations.pop(0)
            nodes.append(parent)
            map_math(weightx, weighty, cost_var, end, graph, default_listdict,
             Mod_internal_Allocations, parent, visited_nodes, next_node, pol)

        output_check = [v for v in (nodes) if v.node == finat_str]

        if (len(output_check) > 0):
            return nodes, output_check[0]
        else:
            return 'Initial/Final Point in Obstacle!!', 0






'''
_________________________________________________________________________________________________________________________________________________________________________________

'''

t = np.linspace(0, 2 * np.pi, 100)

r_cir = 25 #radius of circle
cx_cir = 225  # x-position of the center of the circle
cy_cir = 150  # y-position of the center of the circle
#elip
cx_elip = 150  # x-position of the center 
cy_elip = 100  # y-position of the center
rx_elip = 40  # radius on the x-axis
ry_elip = 20  # radius on the y-axis

#here r_cir is radius of circle
p = cx_cir + r_cir * np.cos(t)
q = cy_cir + r_cir * np.sin(t)

#all possible x and y values for elipse, here r is different
r = cx_elip + rx_elip * np.cos(t)
s = cy_elip + ry_elip * np.sin(t)

x = [225, 250,225, 200]
y = [40, 25, 10, 25]


asx =[95, 30, 35, 100]
asy = [30, 68, 76, 37]


px = [25, 75, 100, 75, 50, 20]
py = [185, 185, 150, 120, 150, 120]


figure, mark = plt.subplots()
mark.grid(color=(0, 0, 0), linestyle='-', linewidth=1)
test = []

xs = []
ys = []

usqx = []
usqy = []
for i in range(4):
    usqx.append(x[i] + radius * np.cos(t))
    usqy.append(y[i] + radius * np.sin(t))

    
urecx = []
urecy = []
for i in range(4):
    urecx.append(asx[i] + radius * np.cos(t))
    urecy.append(asy[i] + radius * np.sin(t))

upolx = []
upoly = []
in_x = []
in_y = []
for i in range(6):
    upolx.append(px[i] + radius * np.cos(t))
    upoly.append(py[i] + radius * np.sin(t))
    mmapx = px[i] + radius * np.cos(t)
    mmapy = py[i] + radius * np.sin(t)
    for j in mmapx:
        in_x.append(j)
    for k in mmapy:
        in_y.append(j)
    upolx.append(mmapx)
    upoly.append(mmapy)

    
ucirx = []
uciry = []
for i in range(len(p)):
    ucirx.append(p[i] + radius * np.cos(t))
    uciry.append(q[i] + radius * np.sin(t))

uelpx = []
uelpy = []
for i in range(len(r)):
    uelpx.append(r[i] + radius * np.cos(t))
    uelpy.append(s[i] + radius * np.sin(t))

ObList = create_Initial(
    [[urecx, urecy,'b'], [asx, asy, 'r'], [usqx, usqy, 'b'], [x, y, 'r'], [upolx, upoly, 'b'], [px, py, 'r'], [ucirx, uciry, 'b'], [p, q, 'r'], [uelpx, uelpy, 'b'], [r, s, 'r']])
'''
__________________________________________________________________________________________________________________________________________________________________________________________

'''


r_cir = 25 / resolution
cx_cir = 225 / resolution  # x-position of the center
cy_cir = 150  / resolution  # radius on the y-axis


cx_elip = 150 / resolution   # x-position of the center 
cy_elip = 100 / resolution  # y-position of the center
rx_elip = 40 / resolution  # radius on the x-axis
ry_elip = 20 / resolution  # radius on the y-axis


#here r_cir is radius of circle
p = cx_cir + r_cir * np.cos(t)
q = cy_cir + r_cir * np.sin(t)

#all possible x and y values for elipse, here r is different
r = cx_elip + rx_elip * np.cos(t)
s = cy_elip + ry_elip * np.sin(t)

x = [225 / resolution, 250 / resolution, 225 / resolution, 200 / resolution]
y = [40 / resolution, 25 / resolution, 10 / resolution, 25/ resolution]

asx =[95 / resolution, 30 / resolution, 35 / resolution, 100 / resolution]
asy = [30 / resolution, 68 / resolution, 76 / resolution, 37 / resolution]

px = [25 / resolution, 75 / resolution, 100 / resolution, 75 / resolution, 50 / resolution, 20 / resolution]
py = [185 / resolution, 185 / resolution, 150 / resolution, 120 / resolution, 150 / resolution, 120]

usqx = []
usqy = []
for i in range(4):
    usqx.append(x[i] + radius * np.cos(t))
    usqy.append(y[i] + radius * np.sin(t))

    
urecx = []
urecy = []
for i in range(4):
    urecx.append(asx[i] + radius * np.cos(t))
    urecy.append(asy[i] + radius * np.sin(t))

upolx = []
upoly = []
in_x = []
in_y = []
for i in range(6):
    upolx.append(px[i] + radius * np.cos(t))
    upoly.append(py[i] + radius * np.sin(t))
    now_x = px[i] + radius * np.cos(t)
    now_y = py[i] + radius * np.sin(t)
    for j in now_x:
        in_x.append(j)
    for k in now_y:
        in_y.append(j)
    upolx.append(now_x)
    upoly.append(now_y)


ucirx = []
uciry = []
for i in range(len(r)):
    ucirx.append(p[i] + radius * np.cos(t))
    uciry.append(q[i] + radius * np.sin(t))

uelpx = []
uelpy = []
for i in range(len(r)):
    uelpx.append(r[i] + radius * np.cos(t))
    uelpy.append(s[i] + radius * np.sin(t))

mark.fill(usqx, usqy, 'b')
mark.fill(x, y, 'r')
mark.fill(urecx, urecy, 'b')
mark.fill(x, y, 'r')
testing = mark.fill(upolx, upoly, 'b')
mark.fill(px, py, 'r')
mark.fill(ucirx, uciry, 'b')
mark.fill(p, q, 'r')
mark.fill(uelpx, uelpy, 'b')
mark.fill(r, s, 'r')


xs = []
ys = []
k = 0
pol = []
for i in testing:
    
    minmax = i.get_xy()
    polygon_vertices = []
    for j in minmax:
        polygon_vertices.append((j[0], j[1]))
    pol.append(polygon_vertices)

obstacles = [[usqx, usqy], [urecx, urecy], [upolx, upoly], [ucirx, uciry], [uelpx, uelpy]]
weightx = [0, 1, 1, 1, 0, -1, -1, -1]
weighty = [1, 1, 0, -1, -1, -1, 0, 1]
cost = [1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2)]

#_____________________________________________________



graph = []

mmapx = start[0]
mmapy = start[1]

pathx = []
pathy = []
paths_to_goal = []

plt.tick_params(axis='both', which='major', labelsize=9)
print("Alogorithm in processing")

nodes, node = dijkstra(graph, str(start[0]) + ' ' + str(start[1]), str(end[0]) + ' ' + str(end[1]), paths_to_goal, mmapx, mmapy, weightx, weighty, cost, end, pol)

if (node == 0):
    test = tk.Tk()
    test.geometry('400x300')
    label = Label(test, text=nodes)
    label.pack()
    test.mainloop()
else:
    ObList = [[usqx, usqy, 'b'], [x, y, 'r'],[urecx, urecy, 'b'], [asx, asy, 'r'], [upolx, upoly, 'b'], [px, py, 'r'], [ucirx, uciry, 'b'], [p, q, 'r'], [uelpx, uelpy, 'b'], [r, s, 'r']]
    test = tk.Tk()
    figure = plt.Figure(figsize=(10, 7), dpi=100)
    mark = figure.add_subplot(111)
    bgcanvas = FigureCanvasTkAgg(figure, test)
    bgcanvas.get_tk_widget().pack(fill=tk.NONE, expand = True)
    

    for i in (ObList):
        mark.fill(i[0], i[1], color=i[2])

    
    mark.grid(color=(0, 0, 0), linestyle='-', linewidth=1)
    
    mark.set_title(title);
    mark.set_xlabel('X axis')
    mark.set_ylabel('Y axis')
    

    final_visual = animation.FuncAnimation(figure, create_Final, nodes, fargs=(nodes, node, test),interval=10, repeat=False, blit = False)

    test.mainloop()






    
