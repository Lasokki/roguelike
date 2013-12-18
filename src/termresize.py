# State for displaying an error message about terminal size

import curses
import curses.wrapper

from state import State

class TermResize(State):

    # Arguments: screen s, dungeon d, player p
    def __init__(self, s):
        self.screen = s
        
    # Field is only temporary
    def draw(self):
        self.screen.erase()
        self.screen.addstr(1, 1, "Resize terminal to at least 80x24, then press q")
        self.screen.refresh()
    
    def handle_input(self, c):
        output = None
        if c == ord('q'):
            output = "basic"
            
        return output
