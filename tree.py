#

class Node():
    def __init__(self, center, dimensions):
        self.children = []; #node can either have 8 node children, 1 poly child or no children at all
        self.center_coor = center; #TODO: the whole isinstance and len error thing
        self.dimensions = dimensions;
    
    def get_children(self):
        return self.children;
    
    def add_child(self, temp):
        self.children.append(temp);
    
    def get_coor(self):
        return self.center_coor;
    
    def get_dimensions(self):
        return self.dimensions;
    
    def get_info(self):
        print(self.children);
        print(self.center_coor);
        print(self.dimensions);
