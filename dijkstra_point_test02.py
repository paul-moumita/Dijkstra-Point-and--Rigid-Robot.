
import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import math
from collections import deque, namedtuple
import sys
from collections import defaultdict
from heapq import *
import matplotlib.animation as animation

from shapely.geometry import Point, Polygon
import time
from ExplorePoint_01 import ToExplore

title = 'Click point in map to select initial point.'

window = tk.Tk()


   
 


start = []
end = []
resolution = 1
radius = 0
clearance = 0

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Border = namedtuple('Border', 'start, end, cost')




def pathAvailability(x, y, minmax, pol):
    """
    Box
    """
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
        print(x,y,'in ellipse')
        return 0
    if ((((math.pow((x - (225 / resolution)), 2)) + (math.pow((y - (150 / resolution)), 2)) - (math.pow(((25 / resolution) + dnd), 2))) <= 0)):
        updateboundaries(x, y, minmax)
        print(x,y,'in circle')
        return 0

    else:

        return 1


def make_edge(start, end, cost=1):
    return Border(start, end, cost)


def test(algo_type):
    pass


def sorting(vals):
    print(vals)
    return vals


def getKey(item):
    return item[0]

def dijkstra(graph, Initial, t, paths_to_goal, pmapx, pmapy, c_weight_x, c_weight_y, costw, end, pol):
        path = []
        paths_to_goal = []

        count = -1
        path = 0
        queue = []
        queue.append((pmapx, pmapy))
        default_listdict = defaultdict(list)

        Mod_internal_allocation, visited_node, mins = [(0, ToExplore(Initial, 0, pmapx, pmapy))], set(), {Initial: 0}
        nodes = []

        count = 0
        while Mod_internal_allocation:
            (cost, v1) = Mod_internal_allocation.pop(0)
            nodes.append(v1)
            direct_to_go(c_weight_x, c_weight_y, costw, end, graph, default_listdict, Mod_internal_allocation, v1, visited_node, mins, pol)

        ans = [v for v in (nodes) if v.node == t]

        if (len(ans) > 0):
            return nodes, ans[0]
        else:
            return 'Initial/end Point in Obstacle!!', 0

         
def onpick(event):
    print(event.xdata, event.ydata)
    global start, end, title
    if (not (start)):
        print('start')
        start = [int(event.xdata), int(event.ydata)]
        title = 'Click point in map to select initial point.'
    else:
        print('end')
        end = [int(event.xdata), int(event.ydata)]
        title = 'Choose algorithm.'
        
    return True


def create_initial(listPnts):
    global title, window, end, start
    
    figure = plt.Figure(figsize=(10, 7), dpi=100)
    mark = figure.add_subplot(111)

    scatter = FigureCanvasTkAgg(figure, window)
    scatter.get_tk_widget().pack(fill=tk.BOTH, expand = True)
    
    mark.fill([300, 0, 0, 300], [200, 200, 0, 0], color=(1, 1, 1))

    for i in (listPnts):
        mark.fill(i[0], i[1], color=i[2])
    
    mark.set_title(title);
    mark.set_xlabel('X axis')
    mark.set_ylabel('Y axis')

    figure.canvas.mpl_connect('button_press_event', onpick)

    tk.Label(window, text="Enter Coordinates").pack()
    tk.Label(window, text="Initial point(comma separated x,y-no spaces)").pack()
    initial = Entry(window)
    if (start):
        init_str = str(start[0]) + ' ' + str(start[1])
        initial.insert(0, init_str)
    initial.pack()
    tk.Label(window, text="end point(comma separated x,y-no spaces)").pack()
    final1 = Entry(window)
    if (end):
        final_str = str(end[0]) + ' ' + str(end[1])
        final1.insert(0, final_str)
    final1.pack()

    tk.Button(window, text="Quit", command=lambda: quit(initial, final1)).pack()

    window.mainloop()
    return listPnts


def animated(i, nodes, node, test):
    if (i):
        if (((nodes[0].x) == i.x) and (nodes[0].y == i.y)):
            mark.scatter(int(i.x), int(i.y), s=5, c='r')
        else:
            mark.scatter(int(i.x), int(i.y), s=5, c='c')

        if (((nodes[len(nodes) - 1].x) == i.x) and (nodes[len(nodes) - 1].y == i.y)):
            node.PrintPath(mark)
        


def quit(initial, final1):
    global window, start, end, radius, resolution, clearance
    resolution = 1
    if (initial.get()):
        x, y = (initial.get()).split(',')
        start = [int(int(x) / resolution), int(int(y) / resolution)]
    elif (start):

        start = [int(start[0] / resolution), int(start[1] / resolution)]
        

    if (final1.get()):
        x1, y1 = (final1.get()).split(',')
        end = [int(int(x1) / resolution), int(int(y1) / resolution)]
    elif (end):
        end = [int(end[0] / resolution), int(end[1] / resolution)]

    radius = 0
    clearance = 0
    window.quit()
    window.destroy()


def direct_to_go(c_weight_x, c_weight_y, cost, end, graph, default_listdict, Mod_internal_allocation, parent, visited_node, mins, pol):
    flag = 0
    pmapx = parent.x
    pmapy = parent.y
    global radius, clearance, resolution

    minx = min(end[0], start[0]) - 1
    miny = min(end[1], start[1]) - 1
    maxx = max(end[0], start[0]) + 1
    maxy = max(end[1], start[1]) + 1

    for i in range(8):

        x = pmapx + c_weight_x[i]
        y = pmapy + c_weight_y[i]

        costw = cost[i]
        a = str(pmapx) + ' ' + str(pmapy)
        b = str(x) + ' ' + str(y)
        tup = (a, b, costw)
        tupin = (b, a, costw)

        if ((tup not in graph) and (tupin not in graph) and (
                x >= 0 and x <= ((300 / resolution) + radius) and y >= 0 and y <= ((200 / resolution) + radius))):

            minmax = [minx, miny, maxx, maxy]
            if ((pathAvailability(x, y, minmax, pol) == 1) and (x >= (minx) and y >= (miny)) and (
                    x <= (maxx) and y <= (maxy))):

                graph.append(tup)
                test.append((x, y))
                if (b not in visited_node):
                    visited_node.add(b)

                    next = (costw + parent.cost)
                    v2 = (ToExplore(b, (next), x, y))
                    v2.parent = parent
                    mins[b] = next
                    Mod_internal_allocation.append((next, v2))
                else:
                    ans = [v for i, v in (Mod_internal_allocation) if v.node == b]
                    prev = mins.get(b, None)
                    next = (costw + parent.cost)
                    if prev is None or next < prev:
                        ans[0].parent = parent
                        mins[b] = next

                        ans[0].cost = next
            else:
                minx = minmax[0]
                miny = minmax[1]
                maxx = minmax[2]
                maxy = minmax[3]


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
for i in range(6):
    upolx.append(px[i] + radius * np.cos(t))
    upoly.append(py[i] + radius * np.sin(t))

    
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

listPnts = create_initial(
    [[urecx, urecy,'k'], [asx, asy, 'r'], [usqx, usqy, 'k'], [x, y, 'r'], [upolx, upoly, 'k'], [px, py, 'r'], [ucirx, uciry, 'k'], [p, q, 'r'], [uelpx, uelpy, 'k'], [r, s, 'r']])
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

mark.fill(usqx, usqy, 'k')
mark.fill(x, y, 'r')
mark.fill(urecx, urecy, 'k')
mark.fill(x, y, 'r')
testing = mark.fill(upolx, upoly, 'k')
mark.fill(px, py, 'r')
mark.fill(ucirx, uciry, 'k')
mark.fill(p, q, 'r')
mark.fill(uelpx, uelpy, 'k')
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
c_weight_x = [0, 1, 1, 1, 0, -1, -1, -1]
c_weight_y = [1, 1, 0, -1, -1, -1, 0, 1]
cost = [1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2)]


graph = []
pmapx = start[0]
pmapy = start[1]

pathx = []
pathy = []
paths_to_goal = []

plt.tick_params(axis='both', which='major', labelsize=9)
print("Alogorithm in processing")

nodes, node = dijkstra(graph, str(start[0]) + ' ' + str(start[1]),str(end[0]) + ' ' + str(end[1]), paths_to_goal, pmapx, pmapy, c_weight_x, c_weight_y, cost, end, pol)

if (node == 0):
    test = tk.Tk()
    test.geometry('400x300')
    label = Label(test, text=nodes)
    label.pack()
    test.mainloop()
else:
    listPnts = [[urecx, urecy,'k'], [asx, asy, 'r'],[usqx, usqy, 'k'], [x, y, 'r'], [upolx, upoly, 'k'], [px, py, 'r'], [ucirx, uciry, 'k'], [p, q, 'r'], [uelpx, uelpy, 'k'], [r, s, 'r']]
    test = tk.Tk()
    figure = plt.Figure(figsize=(10, 7), dpi=100)
    mark = figure.add_subplot(111)
    scatter = FigureCanvasTkAgg(figure, test)
    scatter.get_tk_widget().pack(fill=tk.NONE, expand = True)
    

    for i in (listPnts):
        mark.fill(i[0], i[1], color=i[2])

    
    mark.grid(color=(0, 0, 0), linestyle='-', linewidth=1)
    
    mark.set_title(title);
    mark.set_xlabel('X axis')
    mark.set_ylabel('Y axis')
    

    ani = animation.FuncAnimation(figure, animated, nodes, fargs=(nodes, node, test),interval=10, repeat=False, blit = False)

    test.mainloop()
