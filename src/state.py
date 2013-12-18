# From this class other States are extended.
# There will be a state for:
# - Moving
# - Inventory
# - Help
# - Character screen
# and others, if needed.

import curses
import curses.wrapper

from dungeon import Dungeon
from player import Player

class State(object):

    # Arguments: screen s, dungeon d, player p
    def __init__(self, s, d, p):
        self.screen = s
        self.dungeon = dungeon
        self.player = p;

    #def enter(self):

    def exit(self):
        pass;

    def handle_input(self):
        pass;
        
    def draw(self):
        pass;
