# An NPC for a roguelike
# Erkki Mattila, 2013

class Npc(object):

    def __init__(self, x, y, hp, n = "NPC"):
        self.name = n
        self.coord = [x, y]
        self.hp = hp

    def get_name(self):
        return self.name

    def coord(self):
        return self.coord

    def get_x(self):
        return self.coord[0]

    def get_y(self):
        return self.coord[1]

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp
