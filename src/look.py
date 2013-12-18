# State for looking around

import curses
import curses.wrapper

from state import State
from dungeon import Dungeon
from player import Player

class Look(State):

    """
        __init__
        Arguments: screen s, dungeon d, player p, curses c
    """
    def __init__(self, s, lw, mw, sw, d, p):
        self.screen = s
        self.log_window = lw
        self.map_window = mw
        self.stat_window = sw
        self.dungeon = d
        self.field = self.dungeon.get_field()
        self.player = p
        
        self.x = self.player.get_x()
        self.y = self.player.get_y()
        
        # This variable is used to run parts of draw() only once.
        # There is no need to draw the map over and over again, 
        # when we are just manipulating cursor and log
        self.drawn = False
                
    """
        Basic draw function
    """
    def draw(self):
        
        #DEBUG
        #self.screen.addstr(28, 0, "         turn: " + str(turn) + "        ")
        
        # On the first time when run, draw stuff on map
        #if self.drawn != True :
        self.draw_field(self.map_window, self.field)
        self.draw_items(self.map_window, self.dungeon)
        self.draw_npcs(self.map_window, self.dungeon)
           
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            
        self.map_window.addch(self.player.get_y(), self.player.get_x(), '@', curses.color_pair(1))
        #self.drawn = True
        # self.draw_field(self.map_window, self.field)
        self.display_info()
            
        # Move cursor to y, x
        self.screen.move(self.y+3, self.x+1)
        
        self.log_window.refresh()
        self.map_window.refresh()
        self.stat_window.refresh()
    """
        Method for drawing the terrain of dungeon
        Args: screen, field
    """
    # REFACTOR THIS CRAP RIGHT AWAY
    def draw_field(self, screen, field):

        x = 0
        y = 0
            
        while(y < len(field)):
            while(x < len(field[y])):
                tile = field[y][x]
                if tile.terrain == "wall":
                    screen.addch(y, x, '#')
                elif tile.terrain == "floor":
                    screen.addch(y, x, '.')
                
                x = x + 1
            x = 0
            y = y + 1
            
    """
        Method for drawing items on map
        Args: screen, dungeon
    """
    def draw_items(self, screen, dungeon):
        
        loot = dungeon.get_items()
        
        for coord, loot in loot.items():
            if loot[0].get_name() == "ring":
                screen.addch(coord[1], coord[0], '=')
            elif loot[0].get_name() == "potion":
                screen.addch(coord[1], coord[0], '?')

    """
        Method for drawing npcs on map
        Args: screen, dungeon
    """
    def draw_npcs(self, screen, dungeon):
        
        npcs = dungeon.get_npcs()
        for npc in npcs.itervalues():
            screen.addch(npc.get_y(), npc.get_x(), 'n')  
            
    """
        Method for displaying information about a tile or its occupant(s)
    """
    def display_info(self):
    
        # If coordinates matches PC's, tell something about it
        if self.x == self.player.get_x() and self.y == self.player.get_y() :

            self.log_window.addstr(0, 0, "You see yourself" + "                ")

        else:
            # Ask if there is anything interesting in coordinates
            tile = self.field[self.y][self.x]
            npc = self.dungeon.get_npc_at((self.x, self.y))
            item = self.dungeon.get_item_at((self.x, self.y))
            
            # Priority: npcs, items, terrain
            if npc is not None:
                self.log_window.addstr(0, 0, "You see " + npc.get_name() + "           ")
            elif item is not None:
                self.log_window.addstr(0, 0, "You see items on floor")
            else:
                self.log_window.addstr(0, 0, "You see " + tile.terrain + "           ")
    
    """
        Method for calculating the target coordinates of a command
        Args: command cmd, starting coordinates x and y
    """
    def calc_target(self, cmd, x, y):
        
        target = (x, y)
        
        if cmd == curses.KEY_UP:
            target = (x, y-1)
        elif cmd == curses.KEY_DOWN:
            target = (x, y+1)
        elif cmd == curses.KEY_LEFT:
            target = (x-1, y)
        elif cmd == curses.KEY_RIGHT:
            target = (x+1, y)

        return target
        
    """
        Method all State-objects shold have. Takes a command and handles it.
        Args: command c
    """
    def handle_input(self, c):
     
        output = None

        # Movement
        if c == curses.KEY_UP or c == curses.KEY_DOWN or c == curses.KEY_LEFT or c == curses.KEY_RIGHT:
        
            target = self.calc_target(c, self.x, self.y)
            
            if (target[0] >= 0 and target[1] >= 0) and (len(self.field) > target[1] and len(self.field[0]) > target[0]):
                self.x = target[0]
                self.y = target[1]
          
        # If q is pressed, move back to state Basic
        elif c == ord('q'):
            output = "basic"
            
            #DEBUG
            #self.screen.addstr(25, 0, "                                   ")
            
        return output
        
