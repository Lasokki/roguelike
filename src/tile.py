# Simple tile class for roguelike
# Erkki Mattila, 2013

class Tile(object):

    def __init__(self, t = "wall"):
        self.terrain = t

    def terrain(self):
        return self.terrain
