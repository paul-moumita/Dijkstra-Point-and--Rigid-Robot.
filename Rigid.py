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
title='Click point in map to select Initial/Final point.'
arr=[]
window= tk.Tk()
class Node:
    def __init__(self, node, cost,x,y):
        self.node = node
        self.parent = None
        self.x=x
        self.y=y
        self.cost = cost
        # Print the tree
    def PrintPath(self,mark):
        if self.parent:
            self.parent.PrintPath(mark)
        mark.scatter(self.x,self.y,s=10,c='b')
init=[]
final=[]
resolution=1
radius=0
clearance=1

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

def onclickfetch(event):
    print(event.xdata,event.ydata)
    global init,final,title
    if(not(init)):
        print('init')
        init=[int(event.xdata),int(event.ydata)]
        
    else:
        print('final')
        final=[int(event.xdata),int(event.ydata)]
        
    title='Node Exploration'
    return True

def updateMinMax(arr,minx,miny,maxx,maxy,d):
        if(maxx>arr[2]):
#            print('x max')
            arr[2]=maxx+1+d
        if(minx<arr[0]):
#            print('x min')
            arr[0]=minx-1-d
        if(maxy>arr[3]):
#            print('y max')
            arr[3]=maxy+1+d
        if(miny<arr[1]):
#            print('y min')
            arr[1]=miny-1-d
            
def pathAvailability(x,y,arr,pol,maxPx,minPx,maxPy,minPy):
    """
    Box
    """
    global radius,clearance,resolution
    d=radius+clearance

    if(((y-((76/resolution)+d))<=0) and ((x-((100/resolution)+d))<=0) and ((-y+((30/resolution)-d))<=0) and ((-x+((30/resolution)-d))<=0)):

         maxBx=100
         minBx=30
         maxBy=76
         minBy=30
         
         updateMinMax(arr,minBx,minBy,maxBx,maxBy,d)
         return 0

 
    rec = Point(x,y)




    if(((y-((40/resolution)+d))<=0) and ((x-((250/resolution)+d))<=0) and ((-y+((10/resolution)-d))<=0) and ((-x+((200/resolution)-d))<=0)):

         maxFx=250
         minFx=200
         maxFy=40
         minFy=10
         
         updateMinMax(arr,minFx,minFy,maxFx,maxFy,d)
         return 0

    diamond = Point(x,y)
        
    if(((y-((185/resolution)+d))<=0) and ((x-((100/resolution)+d))<=0) and ((-y+((120/resolution)-d))<=0) and ((-x+((20/resolution)-d))<=0)):

         maxPx=250
         minPx=200
         maxPy=40
         minPy=10
         
         updateMinMax(arr,minPx,minPy,maxPx,maxPy,d)
         return 0

        
    if ((((math.pow((x - (150 / resolution)), 2) / math.pow(((40 / resolution) + d), 2)) + (math.pow((y - (100 / resolution)), 2) / math.pow(((20 / resolution) + d), 2)) - 1) <= 0)):
        maxEx=150+40
        minEx=150-40
        maxEy=100+20
        minEy=100-20
       
        updateMinMax(arr,minEx,minEy,maxEx,maxEy,d)
        
        return 0
    
    if((((math.pow((x-(225/resolution)),2))+(math.pow((y-(150/resolution)),2))-(math.pow(((25/resolution)+d),2)))<=0)):
        maxCx=225+25
        minCx=225-25
        maxCy=150+25
        minCy=150-25
        
        updateMinMax(arr,minCx,minCy,maxCx,maxCy,d)
        
        return 0
    
    else:
        
        return 1
           
def make_edge(start, end, cost=1):
  return Edge(start, end, cost)
def test(algo_type):
  print(algo_type)
def sorting(vals):
    print(vals)
    return vals
def getKey(item):
    return item[0]
def dijkstra(graph,f,t,paths_to_goal,mapx,mapy,weightx,weighty,costw,final,pol):
    path=[]
    paths_to_goal=[]

    
    count=-1
    path=0
    queue=[]
    queue.append((mapx,mapy))
    default = defaultdict(list)
    
    allocation_var,seen,mins,queue= [(0,Node(f,0,mapx,mapy))],set(), {f: 0},[(0,f)]
    nodes=[]

    count=0
    nodes.append(Node(f,0,mapx,mapy))
    node=''
    while (allocation_var and node!=t):
        (cost1,node)=heappop(queue)
       
        index= [i for ((c,y), i) in zip(allocation_var, range(len(allocation_var))) if node==y.node]
        
        (cost,v1) = allocation_var.pop(index[0])
        

        temp_trav(weightx,weighty,costw,final,graph,default,allocation_var,queue,nodes,v1,seen,mins,pol)

    
        
    ans= [v for  v in (nodes) if v.node == t]
    print(ans)
    if(len(ans)>0):
        return nodes,ans[0]
    else:
        return 'Initial/Final Point in Obstacle!!',0
def create_init(listPnts):

    global title,window,final,init
    fig = plt.Figure(figsize=(7,5), dpi=100)
    mark = fig.add_subplot(111)
    
    
    scatter = FigureCanvasTkAgg(fig, window) 
    scatter.get_tk_widget().pack(fill=tk.NONE)
    mark.fill([300,0,0,300],[200,200,0,0], color = (1,1,1))
    
    for i in (listPnts):
        mark.fill(i[0],i[1], color = i[2])

    
    mark.set_title(title);
    mark.set_xlabel('X axis')
    mark.set_ylabel('Y axis')
    

    fig.canvas.mpl_connect('button_press_event',onclickfetch)




    tk.Label(window, text="Enter Coordinates(comma separated x,y-no spaces)").pack()
    tk.Label(window, text="Initial point").pack()
    initial=Entry(window)
    if(init):
        init_str=str(init[0])+' '+str(init[1])
        initial.insert(0,init_str)
    initial.pack()
    tk.Label(window, text="Final point").pack()
    final1=Entry(window)
    if(final):
        final_str=str(final[0])+' '+str(final[1])
        final1.insert(0,final_str)
    final1.pack()

    tk.Button(window, text="Start Processing", command= lambda:quit(initial,final1)).pack()
   
    window.mainloop()
       
    return listPnts

xdata=[]
ydata=[]    
def animated(i,nodes,node,test):
    global xdata,ydata
    t, y = i.x,i.y
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = mark.get_xlim()

    if t >= xmax:
        mark.set_xlim(xmin, 2*xmax)
        mark.figure.canvas.draw()
    line.set_data(xdata, ydata)

    
    
    if(((nodes[len(nodes)-1].x) == i.x) and (nodes[len(nodes)-1].y == i.y)):
          node.PrintPath(mark)
    return line,           

def quit(initial,final1):
    global window,init,final,radius,resolution,clearance,arr

    
    resolution=1
    if(initial.get()):
            if(len((initial.get()).split(','))==2):

                x,y=(initial.get()).split(',')
                if(x and y and (int(x)) and (int(y))):
                    init=[int(int(x)/resolution),int(int(y)/resolution)]
                else:
                    window.quit()
                    window.destroy()
                    test=tk.Tk()
                    test.geometry('400x300')
                    label = Label(test, text= "Please enter valid Initial Point.")

                    label.pack() 

                    test.mainloop()
            else:
                    window.quit()
                    window.destroy()
                    test=tk.Tk()
                    test.geometry('400x300')
                    label = Label(test, text= "Please enter valid comma separated Initial Point.")

                    label.pack() 

                    test.mainloop()

    elif(init):
            
            init=[int(init[0]/resolution),int(init[1]/resolution)]
            
    else:
            window.quit()
            window.destroy()
            test=tk.Tk()
            test.geometry('400x300')
            label = Label(test, text= "Please enter valid Initial Point.")

            label.pack() 

            test.mainloop()

    if(final1.get()):
            if(len((final1.get()).split(','))==2):
                x1,y1=(final1.get()).split(',')
                if(x1 and y1 and (int(x1)) and (int(y1))):
                    final=[int(int(x1)/resolution),int(int(y1)/resolution)]
                else:
                    window.quit()
                    window.destroy()
                    test=tk.Tk()
                    test.geometry('400x300')
                    label = Label(test, text= "Please enter valid Final Point.")

                    label.pack() 

                    test.mainloop()
            else:
                    window.quit()
                    window.destroy()
                    test=tk.Tk()
                    test.geometry('400x300')
                    label = Label(test, text= "Please enter valid comma separated Final Point.")

                    label.pack() 

                    test.mainloop()
    elif(final):
                final=[int(final[0]/resolution),int(final[1]/resolution)]

    else:
                window.quit()
                window.destroy()
                test=tk.Tk()
                test.geometry('400x300')
                label = Label(test, text= "Please enter valid Final Point.")

                label.pack() 

    
                test.mainloop()
    if((rad.get()) and (int(int(rad.get())/resolution))>=0):
            radius=int(int(rad.get())/resolution)
        else:
            window.quit()
            window.destroy()
            test=tk.Tk()
            test.geometry('400x300')
            label = Label(test, text= "Please enter valid Radius.")

            label.pack() 

            test.mainloop()
        if((clr.get()) and (int(int(clr.get())/resolution))>=0):
            clearance=int(int(clr.get())/resolution)
            window.quit()
            window.destroy()
            minx = min(final[0],init[0])-1
            miny = min(final[1],init[1])-1
            maxx= max(final[0],init[0])+1
            maxy= max(final[1],init[1])+1
            arr=[minx,miny,maxx,maxy]
        else:
            window.quit()
            window.destroy()
            test=tk.Tk()
            test.geometry('400x300')
            label = Label(test, text= "Please enter valid Clearance.")

            label.pack() 

            test.mainloop()
    else:
        window.quit()
        window.destroy()
        test=tk.Tk()
        test.geometry('400x300')
        label = Label(test, text= "Please enter valid Resolution.")

        label.pack() 

        test.mainloop()    
def temp_trav(weightx,weighty,cost,final,graph,default,allocation_var,queue,nodes,parent,seen,mins,pol):
    global arr,maxPx,minPx,maxPy,minPy
    flag=0
    mapx=parent.x
    mapy=parent.y
    global radius,clearance,resolution
    d=radius+clearance
    minx = min(final[0],init[0])-1
    miny = min(final[1],init[1])-1
    maxx= max(final[0],init[0])+1
    maxy= max(final[1],init[1])+1

    for i in range(8):
                
                x=mapx+weightx[i]
                y=mapy+weighty[i]

                costw=cost[i]
                parent_var=str(mapx)+' '+str(mapy)
                node_var=str(x)+' '+str(y)
                tup=(parent_var,node_var,costw)
                tupin=(node_var,parent_var,costw)
                

                if((tup not in graph) and (tupin not in graph) and (x>=0 and x<=((300/resolution)+radius) and y>=0 and y<=((200/resolution)+radius)) and (((x+d)<=(300/resolution)) and ((y+d)<=(200/resolution)) and ((x-d)>=(0/resolution)) and ((y-d)>=(0/resolution)))):


                    

                    if(((pathAvailability(x,y,arr,pol,maxPx,minPx,maxPy,minPy))==1) and (x>=(arr[0]) and y>=(arr[1])) and ( x<=(arr[2]) and y<=(arr[3]) )):

                        graph.append(tup)

                        test.append((x,y))


                        if(node_var not in seen):
                            seen.add(node_var)
                            
                            next = (costw+parent.cost)
                            v2=(Node(node_var,(next),x,y))
                            v2.parent=parent
                            mins[node_var] = next
                            nodes.append(v2)
                            allocation_var.append((next,v2))
                            heappush(queue, (next, node_var))
                        else:
                            ans= [v for v in (nodes) if v.node == node_var]
                            # ans1= [i for i, v in (queue) if v == node_var]
                            prev = mins.get(node_var, None)
                            next = (costw+parent.cost)
                            if prev is None or next < prev:
                                    ans[0].parent=parent
                                    mins[node_var] = next
                                    
                                    ans[0].cost=next

                    else:
                        minx=arr[0]
                        miny=arr[1]
                        maxx=arr[2]
                        maxy=arr[3]
                    
 
    
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


fig, mark = plt.subplots()
mark.grid(color=(0,0,0), linestyle='-', linewidth=1)
test=[]



xs=[]
ys=[]

uboxx=[]
uboxy=[]
for i in range(4):
    uboxx.append(x[i]+radius*np.cos(t))
    uboxy.append(y[i]+radius*np.sin(t))


urecx = []
urecy = []
for i in range(4):
    urecx.append(asx[i] + radius * np.cos(t))
    urecy.append(asy[i] + radius * np.sin(t))


upolx=[]
upoly=[]
for i in range(6):
    upolx.append(px[i]+radius*np.cos(t))
    upoly.append(py[i]+radius*np.sin(t) )
    
ucirx=[]
uciry=[]
for i in range(len(r)):
    ucirx.append(p[i]+radius*np.cos(t))
    uciry.append(q[i]+radius*np.sin(t))
    
uelpx=[]
uelpy=[]
for i in range(len(r)):
    uelpx.append(r[i]+radius*np.cos(t))
    uelpy.append(s[i]+radius*np.sin(t))

listPnts=create_init([[urecx, urecy,'k'], [asx, asy, 'r'],[uboxx, uboxy,'k'],[x, y,'r'],[upolx, upoly,'k'], [px, py,'r'],[ucirx, uciry,'k'],[p,q,'r'],[uelpx, uelpy,'k'],[r,s,'r']])
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




uboxx=[]
uboxy=[]
for i in range(4):
    uboxx.append(x[i]+radius*np.cos(t))
    uboxy.append(y[i]+radius*np.sin(t) )

urecx = []
urecy = []
for i in range(4):
    urecx.append(asx[i] + radius * np.cos(t))
    urecy.append(asy[i] + radius * np.sin(t))


upolx=[]
upoly=[]
in_x=[]
in_y=[]
for i in range(6):
    temp_x=px[i]+radius*np.cos(t)
    temp_y=py[i]+radius*np.sin(t) 
    for j in temp_x:
        in_x.append(j)
    for k in temp_y:
        in_y.append(j)
    upolx.append(temp_x)
    upoly.append(temp_y)



ucirx=[]
uciry=[]
for i in range(len(r)):
    ucirx.append(p[i]+radius*np.cos(t))
    uciry.append(q[i]+radius*np.sin(t))
    
uelpx=[]
uelpy=[]
for i in range(len(r)):
    uelpx.append(r[i]+radius*np.cos(t))
    uelpy.append(s[i]+radius*np.sin(t))

mark.fill(uboxx, uboxy,'k')
mark.fill(x, y,'r')
mark.fill(urecx, urecy, 'k')
mark.fill(x, y, 'r')

testing=mark.fill(upolx, upoly,'k')
mark.fill(px, py,'r')
mark.fill(ucirx, uciry,'k')
mark.fill(p,q,'r')
mark.fill(uelpx, uelpy,'k')
mark.fill(r,s,'r')


xs=[]
ys=[]
k=0
pol=[]
for i in testing:

    array=i.get_xy()

    polygon_vertices=[]
    for j in array:


        polygon_vertices.append((j[0],j[1]))

    pol.append(polygon_vertices)



maxPx=0
minPx=300
maxPy=0
minPy=200


for i in pol:
        coords = i
        poly = Polygon(i)
        for j in i:
            
            if(minPx>j[0]):
                minPx=j[0]
            if(maxPx<j[0]):
                maxPx=j[0]
            if(minPy>j[1]):
                minPy=j[1]
            if(maxPy<j[1]):
                maxPy=j[1]

                
print(minPx,minPy,maxPx,maxPy)


obstacles=[[urecx, urecy],[uboxx, uboxy],[upolx, upoly],[ucirx, uciry],[uelpx, uelpy]]
weightx=[0,1,1,1,0,-1,-1,-1]
weighty=[1,1,0,-1,-1,-1,0,1]
cost=[1,np.sqrt(2),1,np.sqrt(2),1,np.sqrt(2),1,np.sqrt(2)]

graph=[]
mapx=init[0]
mapy=init[1]


pathx=[]
pathy=[]
paths_to_goal=[]

plt.tick_params(axis='both', which='major', labelsize=9)
print("Processing.....")
if(init and final):
    nodes,node=dijkstra(graph,str(init[0])+' '+str(init[1]),
                            str(final[0])+' '+str(final[1]),paths_to_goal,mapx,mapy,weightx,weighty,cost,final,pol)
    if(node==0):
        test=tk.Tk()
        test.geometry('400x300')
        label = Label(test, text= nodes)

        label.pack() 

        test.mainloop()
    else:
        listPnts=[[urecx, urecy,'k'], [asx, asy, 'r'],[uboxx, uboxy,'b'],[x, y,'r'],[upolx, upoly,'b'], [px, py,'r'],[ucirx, uciry,'b'],[p,q,'r'],[uelpx, uelpy,'b'],[r,s,'r']]
        test=tk.Tk()
        fig = plt.Figure(figsize=(7,5), dpi=100)
        mark = fig.add_subplot(111)
        
        line, = mark.plot([], [], 'y.', lw=0.3, alpha=0.2)
        mark.grid()

        scatter = FigureCanvasTkAgg(fig, test) 
        scatter.get_tk_widget().pack(fill=tk.NONE)
    
        for i in (listPnts):
                mark.fill(i[0],i[1], color = i[2])
                    

        
        mark.grid(color=(0,0,0), linestyle='-', linewidth=1) 

        mark.set_title(title);
        mark.set_xlabel('X axis')
        mark.set_ylabel('Y axis')

        ani = animation.FuncAnimation(fig, animated, nodes, fargs=(nodes, node,test), interval=10,repeat=False, blit=False)



    
        test.mainloop()
else:
        test=tk.Tk()
        test.geometry('400x300')
        label = Label(test, text= "Please check validity if Initial/Goal Coordinates, Resolution, Radius or Clearance.")

        label.pack() 

        test.mainloop()
