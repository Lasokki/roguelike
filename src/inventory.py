# State for manipulating inventory

import curses
import curses.wrapper

from state import State
from dungeon import Dungeon
from player import Player

class Inventory(State):

    # Arguments: screen s, dungeon d, player p
    def __init__(self, s, d, p):
        self.screen = s
        self.dungeon = d
        self.player = p
        
    # Field is only temporary
    def draw(self):

        inventory = self.player.get_inventory()

        self.screen.addstr(1, 5, "Inventory")
        
        i = 2
        for thing, count in inventory.items():
            thingstring = thing + " " + str(count)
            self.screen.addstr(i, 5, thingstring)
            i += 1
        
        self.screen.refresh()
    
    def handle_input(self, c):
        output = None
        if c == ord('q'):
            output = "basic"
            
        return output
