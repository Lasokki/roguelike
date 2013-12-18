# Basic state
# - Moving
# - Attacking

import curses
import curses.wrapper

from state import State
from dungeon import Dungeon
from player import Player

class Basic(State):    

    def __init__(self, s, lw, mw, sw, d, p):
        self.screen = s
        self.log_window = lw
        self.map_window = mw
        self.stat_window = sw
        self.dungeon = d;
        self.field = self.dungeon.get_field()
        self.player = p;
    
    # Args: command c
    def handle_input(self, c):
    
        output = None
        
        # Picking up: check if there is anything to pick
        if c == ord(',') and self.dungeon.get_item_at((self.player.get_x(), self.player.get_y())) is not None:
            self.execute_action(c, self.player, self.dungeon)

        # Inventory
        elif c == ord('i'):
            output = "inventory"
            
        # Looking
        elif c == ord('l'):
            output = "look"
            
        # Movement
        elif c == curses.KEY_UP or c == curses.KEY_DOWN or c == curses.KEY_LEFT or c == curses.KEY_RIGHT:
            self.execute_action(c, self.player, self.dungeon)
        
        # Quitting
        elif c == ord('q'):
            output = "quit"
            
        return output

    """
    Start of drawing related functions
    """

    # Basic draw function
    # Still can't figure out why the screen is black before input
    def draw(self):
        
        #DEBUG
        #self.screen.addstr(28, 0, "         turn: " + str(turn) + "        ")
        
        self.draw_field(self.map_window, self.field)
        #self.draw_items(self.map_window, self.dungeon)
        #self.draw_npcs(self.map_window, self.dungeon)
        """
        self.log_window.noutrefresh()
        self.map_window.noutrefresh()
        self.stat_window.noutrefresh()
        curses.doupdate()
        """
        self.log_window.noutrefresh()
        self.map_window.noutrefresh()
        self.stat_window.noutrefresh()

    # REFACTOR THIS CRAP RIGHT AWAY
    def draw_field_old(self, screen, field):

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
    Prints 79x17 tiles of a given field, centered on player.
    """
    # REFACTOR THIS ASAP
    def draw_field(self, window, field):
       
        center_x = self.player.get_x()
        center_y = self.player.get_y()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.log_window.addstr(1,0, "x " + str(center_x))
        self.log_window.addstr(2,0, "y " + str(center_y))

        self.log_window.addstr(1, 20, str(len(field[0])))
        self.log_window.addstr(2, 20, str(len((field))))

        if center_x-39 < 0:
            self.log_window.addstr(0,0, "x_0")
            start_x = 0
        
        elif center_x+39 < len(field[0]):
            start_x = center_x - 39
            self.log_window.addstr(0,0, "x_center")

        else:
            start_x = len(field[0])-78
            self.log_window.addstr(0,0, "x_leftside")

        if center_y-8 < 0:
            start_y = 0
            self.log_window.addstr(0,10, "y_0")

        elif center_y+8 < len(field):
            start_y = center_y - 8
            self.log_window.addstr(0,10, "y_center")

        else:
            start_y = len(field)-16
            self.log_window.addstr(0,10, "y_bottom")

        x = 0
        y = 0
        field_y = start_y
        self.log_window.addstr(1, 30, str(start_x))
        self.log_window.addstr(2, 30, str(start_y))

        while (y < 16):
            field_x = start_x
            while (x < 78):
                tile = field[field_y][field_x]
                if tile.terrain == "wall":
                    window.addch(y, x, '#')
                elif tile.terrain == "floor":
                    window.addch(y, x, '.')
                
                x = x + 1
                # if field_x + 1 < len(field[0]):
                field_x = field_x + 1
            x = 0
            # if field_y + 1 < len(field):
            field_y = field_y + 1
            y = y + 1        

        # Come up with better names
        player_x = None
        player_y = None

        # Check if player is not near edges of map
        if center_x-39 > 0 and center_x+39 < len(field[0]):
            player_x = 39

        else:
            # If player is near the left side of the map, do simple things
            if self.player.get_x() < 79:
                player_x = self.player.get_x()
            # If player is near the right side of the map, do tricky things
            else:
                player_x = 78 + (self.player.get_x() - len(field[0]))

        # Apply principles from x-axis to y-axis
        if center_y-8 > 0 and center_y+8 < len(field):
            player_y = 8

        else:
            if self.player.get_y() < 17:
                player_y = self.player.get_y()
            else:
                player_y = 16 + (self.player.get_y() - len(field))

        if player_y is not None and player_x is not None:
            window.addch(player_y, player_x, '@', curses.color_pair(1))

    def draw_items(self, screen, dungeon):
        
        loot = dungeon.get_items()
        
        for coord, loot in loot.items():
            if loot[0].get_name() == "ring":
                screen.addch(coord[1], coord[0], '=')
            elif loot[0].get_name() == "potion":
                screen.addch(coord[1], coord[0], '?')

    def draw_npcs(self, screen, dungeon):
        
        npcs = dungeon.get_npcs()
        for npc in npcs.itervalues():
            screen.addch(npc.get_y(), npc.get_x(), 'n')


    """
    End of drawing related functions
    """
    
    # Args: actor, dungeon
    def pick_up_item(self, actor, dungeon):

        x = actor.get_x()
        y = actor.get_y()
        
        # pick up the top item
        item = dungeon.get_item_at((x, y))[0]
        actor.add_to_inv(item)
        dungeon.remove_item((x, y))
        log = "You pick up a " + item.get_name() + "."
        return log

    # Args: command, target x, target y
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

    # Args: target, dungeon, screen (debug)
    def hit(self, target, dungeon):
        
        npc = dungeon.get_npc_at(target)

        npc.set_hp(npc.get_hp() - 1)
        log =  "You promptly hit the " + npc.get_name() + "."

        if npc.get_hp() <= 0:
            dungeon.remove_npc(target)
            log = "You slay the foul " + npc.get_name() + "!"

        return log

    # Args: target, field
    def check_ahead(self, target, field):

        passable = True
        if field[target[1]][target[0]].terrain != "floor":
            passable = False

        return passable

    """ 
        Currently a general function for actions.
        Idea: Actors usually have one action per turn.

        Possible structure for execute_action:
        - non-movement actions
        - movement-related actions
        
        Actions could return a string to log? log = log + " " + action(derp)

        NOTE DEBUG: argument screen

    """

    # Arguments: command, actor, dungeon, screen (debug)
    def execute_action(self, cmd, actor, dungeon):
        
        # Erase old stuff from log_window
        self.log_window.erase()
        log = ""

        # Check for non-movement command
        if cmd == ord(','):
            log = log + self.pick_up_item(actor, dungeon) + " "

        else:

            # Actor targets coordinates (x, y)
            target = self.calc_target(cmd, actor.get_x(), actor.get_y())

            npc = dungeon.get_npc_at(target)

            # Attack, if possible
            if npc is not None:            
                log = log + self.hit(target, dungeon) + " "
               
            # Move, if possible
            # Idea: Change so that something is written to log for bumps and stepping to new terrain
            elif self.check_ahead(target, dungeon.get_field()):

                actor.set_x(target[0])
                actor.set_y(target[1])
        
        self.log_window.addstr(0,0, log)
