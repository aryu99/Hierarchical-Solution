class Agent:
    def __init__(self, id, x, y, shelf, flag):
        '''
        Parameters
        ----------
        id : int
            The id of the agent
        x : int
            The x coordinate of the agent
        y : int
            The y coordinate of the agent
        shelf : int
            The id of the shelf the agent is carrying (0 if not carrying anything)
        flag : int
            Whether it is an empty shelf (0) or a full shelf (1)
        action: None or Action
        '''
        self.id = id
        self.x = x
        self.y = y
        self.shelf = shelf
        self.flag = flag
        if self.shelf == 0:
            assert self.flag == 0
        self.action = None

    def __str__(self):
        return "Agent {}: ({}, {})".format(self.id, self.x, self.y)
    
    def set_shelf(self, shelf):
        self.shelf = shelf
    
    def toggle_flag(self, flag):
        self.flag = flag

class Shelf:
    def __init__(self, id, x, y, req, pos):
        '''
        Parameters
        ----------
        id : int
            The id of the shelf
        unique_coord: tuple
            The unique initial coordinates of the shelf
        x : int
            The x coordinate of the shelf (gets reset to the place where an agent drops it at)
        y : int
            The y coordinate of the shelf
        req : int
            Whether it is a requested shelf (1) or not (0)
        pos : int
            Position of the shelf. 0 if it is not on an agent, otherwise the id of the agent it is on.
        '''
        self.id = id
        self.unique_coord = (x, y)
        self.x = x
        self.y = y
        self.req = req
        self.pos = pos

    def __str__(self):
        return "Shelf {}: ({}, {})".format(self.id, self.x, self.y)
    
    def toggle_flag(self, flag):
        self.flag = flag
    
    def set_pos(self, pos):
        self.pos = pos