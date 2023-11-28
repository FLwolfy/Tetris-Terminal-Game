class BaseBlock:
    def __init__(self, x:int=8, y:int=-4):
        # the base shape needs to be n*n
        self.base_shape = \
            [["\u25A0", "\u25A0", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A0", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A0", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A0", "\u25A0", "\u25A0"]]

        # The top left corner coords
        self.x = x
        self.y = y
        
        # Rotation index
        self.current_direction = 0
        
    @property
    # The four directional shape
    def shapes(self)->list[list[list[str]]]:
        return \
            [self.base_shape,
             [row for row in list(zip(*self.base_shape))[::-1]], # zip(*list) means the transpose of the list
             [row[::-1] for row in self.base_shape[::-1]], 
             [row[::-1] for row in zip(*self.base_shape)]]

    # rotate the current block counterclockwise by 90 degree
    def rotateLeft(self)->None:
        # your code here
        if(self.current_direction == 3):
            self.current_direction = 0
        else:
            self.current_direction += 1
        return
    
    # rotate the current block clockwise by 90 degree
    def rotateRight(self)->None:
        # your code here
        if(self.current_direction == 0):
            self.current_direction = 3
        else:
            self.current_direction -= 1
        return
    
    # move the current block downward by one
    def moveDown(self)->None:
        # your code here
        self.y += 1
        return
    
    # move the current block rightward by one
    def moveRight(self)->None:
        # your code here
        self.x += 1
        return
    
    # move the current block leftward by one 
    def moveLeft(self)->None:
        # your code here
        self.x -= 1
        return
    
    # return current shape of the block
    def getShape(self)->list[list[str]]:
        return self.shapes[self.current_direction]

class IBlock(BaseBlock):
    def __init__(self):
        super().__init__()
        self.base_shape = \
            [["\u25A0", "\u25A3", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A0", "\u25A0"]]
            
class JBlock(BaseBlock):
    def __init__(self):
        super().__init__()
        self.base_shape = \
            [["\u25A0", "\u25A0", "\u25A3", "\u25A0"],
             ["\u25A0", "\u25A0", "\u25A3", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A3", "\u25A0"],
             ["\u25A0", "\u25A0", "\u25A0", "\u25A0"]]

class LBlock(BaseBlock):
    def __init__(self):
        super().__init__()
        self.base_shape = \
            [["\u25A0", "\u25A3", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A3", "\u25A0"],
             ["\u25A0", "\u25A0", "\u25A0", "\u25A0"]]

class OBlock(BaseBlock):
    def __init__(self):
        super().__init__()
        self.base_shape = \
            [["\u25A3", "\u25A3"],
             ["\u25A3", "\u25A3"]]

class ZBlock(BaseBlock):
    def __init__(self):
        super().__init__()
        self.base_shape = \
            [["\u25A0", "\u25A0", "\u25A0"],
             ["\u25A3", "\u25A3", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A3"]]
            
class TBlock(BaseBlock):
    def __init__(self):
        super().__init__()
        self.base_shape = \
            [["\u25A0", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A0"],
             ["\u25A3", "\u25A3", "\u25A3"]]

class SBlock(BaseBlock):
    def __init__(self):
        super().__init__()
        self.base_shape = \
            [["\u25A0", "\u25A0", "\u25A0"],
             ["\u25A0", "\u25A3", "\u25A3"],
             ["\u25A3", "\u25A3", "\u25A0"]]
