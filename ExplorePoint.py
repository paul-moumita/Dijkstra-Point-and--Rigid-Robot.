
#Exploring Nodes in the Map
class ToExplore:
    def __init__(self, node, cost, x, y):
        self.node = node
        self.parent = None
        self.x = x
        self.y = y
        self.cost = cost

    # Print the tree
    def PrintPath(self, mark):
        if self.parent:
            self.parent.PrintPath(ax)
        mark.scatter(self.x, self.y, s=5, c='k')

   
    def updateboundaries(x, y, d, minmax):
        if(x>minmax[2]):
            minmax[2]=x+1+d
        if(x<minmax[0]):
            minmax[0]=x-1-d
        if(y>minmax[3]):
            minmax[3]=y+1+d
        if(y<minmax[1]):
            minmax[1]=y-1-d
