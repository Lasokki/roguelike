# Simple player
# Erkki Mattila, 2013

class Player(object):

    def __init__(self, x = 10, y = 10, n = "Oi, you!"):
        self.name = n
        self.coord = [x, y]
        self.inventory = {}

    def name(self):
        return self.name

    def coord(self):
        return self.coord

    def get_inventory(self):
        return self.inventory

    def add_to_inv(self, k):
        if k.get_name() in self.inventory:
            self.inventory[k.get_name()] += 1
        else:
            new = {k.get_name() : 1}
            self.inventory.update(new)

    def set_x(self, x):
        self.coord[0] = x

    def get_x(self):
        return self.coord[0] 
    
    def get_y(self):
        return self.coord[1] 
    
    def set_y(self, y):
        self.coord[1] = y
