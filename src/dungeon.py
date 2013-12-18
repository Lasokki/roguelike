# Class for dungeons
# Simple roguelike in python
# Erkki Mattila, 2013

from tile import Tile
from npc import Npc
from item import Item

class Dungeon(object):

    def __init__(self):
        self.field = self.create_field()
        self.npcs = self.create_npcs()
        self.items = {}

    def create_field(self):
        field = []
        for y in range(0, 32):
            m = []
            for x in range(0, 157):
                m.append(Tile())
            field.append(m)
        
        for y in range(1, 31):
            for x in range(1, 156):
                if (y < 31 and  y > 28) or (y > 0 and y < 3):
                    if x % 3 != 0:
                        field[y][x] = Tile("floor")
                else:
                    field[y][x] = Tile("floor")

        return field
    
    def create_npcs(self):
        npcs = {}
        npc = Npc(7, 7, 10, "small n")
        coord = (npc.get_x(), npc.get_y())
        npcs = { coord : npc }
        return npcs

    def create_item(self, x, y, name):
        coord = (x, y)
        item = Item(name)

        if coord in self.items:
            self.items[coord].append(item)
        else:
            self.items[coord] = [item]

    def get_item_at(self, coord):
        item = self.items.get(coord)
        return item

    def remove_item(self, coord):
        del self.items[coord]

    def get_npc_at(self, coord):
        npc = self.npcs.get(coord)
        return npc

    # removes npc at coordinates (x, y)
    def remove_npc(self, coord):
        del self.npcs[coord]

    def get_field(self):
        return self.field

    def get_npcs(self):
        return self.npcs

    def get_items(self):
        return self.items
