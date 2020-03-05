import tkinter as tk
from tkinter import *
import numpy as np
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
Border = namedtuple('Border', 'initial, final, cost')

'''
##--------------------------------------------------------------------------------------##
##Functions will be defined here##
##--------------------------------------------------------------------------------------##
'''
