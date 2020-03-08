class Node:
    def __init__(self, node, location, parent=None, cost=float("inf")):                         
        self.node = node
        self.parent = parent
        self.location = location
        self.cost = cost
