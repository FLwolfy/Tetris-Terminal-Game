class BaseBlock:
    def __init__(self, x:int = 0, y:int = -4):
        # the base shape needs to be n*n (smaller than 4*4)
        self.base_shape = \
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]

        # the top left corner coords (borders don't count as coordinates)
        self.x = x
        self.y = y
        
        # rotation index
        self.current_direction = 0
        
        # whether the block is special or not
        self.is_special = False
        
    @property
    def shapes(self)->list[list[list[int]]]:
        '''
        The four directional shape
        '''
        return \
            [self.base_shape,
             [list(row) for row in list(zip(*self.base_shape))[::-1]], # zip(*list) means the transpose of the list
             [row[::-1] for row in self.base_shape[::-1]], 
             [list(row[::-1]) for row in zip(*self.base_shape)]]

    def rotateLeft(self)->None:
        '''
        rotate the current block counterclockwise by 90 degree
        '''
        if(self.current_direction == 3):
            self.current_direction = 0
        else:
            self.current_direction += 1
        return
    
    def rotateRight(self)->None:
        '''
        rotate the current block clockwise by 90 degree
        '''
        if(self.current_direction == 0):
            self.current_direction = 3
        else:
            self.current_direction -= 1
        return
    
    def moveDown(self)->None:
        '''
        move the current block downward by one
        '''
        self.y += 1
        return
    
    def moveRight(self)->None:
        '''
        move the current block rightward by one
        '''
        self.x += 1
        return
    
    def moveLeft(self)->None:
        '''
        move the current block leftward by one 
        '''
        self.x -= 1
        return
    
    def getShape(self)->list[list[int]]:
        '''
        return current shape of the block
        '''
        return self.shapes[self.current_direction]

class IBlock(BaseBlock):
    def __init__(self, x:int, y:int = -3):
        super().__init__(x, y)
        self.base_shape = \
            [[0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
            
class JBlock(BaseBlock):
    def __init__(self, x:int, y:int = -3):
        super().__init__(x, y)
        self.base_shape = \
            [[0, 1, 0],
             [0, 1, 0],
             [1, 1, 0]]

class LBlock(BaseBlock):
    def __init__(self, x:int, y:int = -3):
        super().__init__(x, y)
        self.base_shape = \
            [[0, 1, 0],
             [0, 1, 0],
             [0, 1, 1]]

class OBlock(BaseBlock):
    def __init__(self, x:int, y:int = -3):
        super().__init__(x, y)
        self.base_shape = \
            [[1, 1],
             [1, 1]]

class ZBlock(BaseBlock):
    def __init__(self, x:int, y:int = -3):
        super().__init__(x, y)
        self.base_shape = \
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]]
            
class TBlock(BaseBlock):
    def __init__(self, x:int, y:int = -3):
        super().__init__(x, y)
        self.base_shape = \
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]]

class SBlock(BaseBlock):
    def __init__(self, x:int, y:int = -3):
        super().__init__(x, y)
        self.base_shape = \
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]]
            

