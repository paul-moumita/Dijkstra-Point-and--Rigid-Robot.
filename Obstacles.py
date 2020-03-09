#Available path
def Path_Availability(x,y,resolution, clearance=0):
	global radius, clearance, resolution
    dnd = radius + clearance
	within_rectangle = (((y - ((76 / resolution) + dnd)) <= 0) and ((x - ((100 / resolution) + dnd)) <= 0) and ((-y + ((30 / resolution) - dnd)) <= 0) and ((-x + ((30 / resolution) - dnd)) <= 0)):
    within_circle = ((((math.pow((x - (225 / resolution)), 2)) + (math.pow((y - (50 / resolution)), 2)) - (math.pow(((25 / resolution) + dnd), 2))) <= 0)):
    within_Ellipse = ((((math.pow((x - (150 / resolution)), 2) / math.pow(((40 / resolution) + dnd), 2)) + (math.pow((y - (100 / resolution)), 2) / math.pow(((20 / resolution) + dnd), 2)) - 1) <= 0)):
    within_kite = (((y - ((40 / resolution) + dnd)) <= 0) and ((x - ((250 / resolution) + dnd)) <= 0) and ((-y + ((10 / resolution) - dnd)) <= 0) and ((-x + ((200 / resolution) - dnd)) <= 0)):
          