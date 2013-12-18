# A simple curses test 
# Erkki Mattila, 2013

import curses
import curses.wrapper

from state import State
from basic import Basic
from inventory import Inventory
from dungeon import Dungeon
from player import Player
from look import Look
from termresize import TermResize
            
"""

   Main function, which contains main loop.
   
   Idea: Separate functionality into State-objects, which will have:
   -state.draw()
   -state.process(command)
"""

def main(stdscr):

    curses.curs_set(0)
    curses.start_color()
    curses.initscr()

    # Create windows for log (lines 1-3), map (lines 4-20) and stats (lines 21-24).
    log_window = curses.newwin(3, 79, 0, 1)
    map_window = curses.newwin(17, 79, 3, 1)
    stat_window = curses.newwin(4, 79, 20, 1)

    dungeon = Dungeon()
    
    dungeon.create_item(7, 9, "ring")
    dungeon.create_item(10, 12, "ring")
    dungeon.create_item(20, 10, "potion")
    
    player = Player()
    
    state = Basic(stdscr, log_window, map_window, stat_window, dungeon, player)
    new_state = None
        
    while 1:
        
        window_size = stdscr.getmaxyx()
        
        # Check if the terminal size is botched - refactor when you understand curses better
         
        if  window_size[0] < 24 or window_size[1] < 80:
            state = create_state("termresize", stdscr, log_window, map_window, stat_window, dungeon, player)
            state.draw()
            curses.doupdate()
            c = stdscr.getch()
        
        else:
        
            # Cargoculted on Monday morning, 05:00.
            # Not doing this initscr() will result in a black screen before first keypress when moving
            # to a new state. No idea what causes this. Will do for now.
            if new_state is not None:
                curses.initscr()

            state.draw()
            curses.doupdate()
        
            c = stdscr.getch()
        
            new_state = state.handle_input(c)
       
            if new_state is not None:
                if new_state == "quit" :
                    break
                else:
                    state = create_state(new_state, stdscr, log_window, map_window, stat_window, dungeon, player)
                    stdscr.erase()
                    #clear_screen(stdscr, dungeon.get_field())
                
def create_state(new_state, screen, log_window, map_window, stat_window, dungeon, player):

    curses.curs_set(0)
    
    if new_state == "basic" :
        output = Basic(screen, log_window, map_window, stat_window, dungeon, player)
    elif new_state == "inventory" :
        output = Inventory(map_window, dungeon, player)
    elif new_state == "look" :
        output = Look(screen, log_window, map_window, stat_window, dungeon, player)
        curses.curs_set(1)
    elif new_state == "termresize" :
        output = TermResize(map_window)
    
    return output
    
# REFACTOR REFACTOR REFACTOR
def clear_screen(screen, field):

    x = 0
    y = 0

    while (y < len(field)):
        while (x < len(field[y])):
            screen.addch(y, x, ' ')
            x += 1
        x = 0
        y += 1
        
if __name__ == "__main__":
    curses.wrapper(main)
    print "Until next time"
