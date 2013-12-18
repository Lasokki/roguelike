# A simple item
# Erkki Mattila, 2013

class Item(object):
    
    def __init__(self, n="item"):
        self.name = n

    def set_name(self, n):
        self.name = n

    def get_name(self):
        return self.name
