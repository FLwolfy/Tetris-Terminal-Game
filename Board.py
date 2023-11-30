from Globals import *
from Block import *
import random

class Board:
    def __init__(self, height: int = 15, width : int = 20, special_block_rate: float = 0):
        self.special_block_rate = special_block_rate
        
        self.__height = height
        self.__width = width
        self.__cur_block = BaseBlock()
        self.__next_block = BaseBlock()
        self.__board = [[-1] * (self.__width + 2) for _ in range(8)] + \
                       [[-1] + [0] * (self.__width) + [-1] for _ in range(self.__height)] + \
                       [[-1] * (self.__width + 2) for _ in range(2)]
        self.__stretch_board_record = [[-1] + [0] * (self.__width + 1) for _ in range(self.__height + 10)]
        self.__records = []
        self.__current_record_index = 1 
        self.__pause_shape = \
            [[1, 1, 1, 1],
             [1, 0, 0, 1],
             [1, 1, 1, 1],
             [1, 0, 0, 0]] # has to be 4*4
        
        # twice to generate random for both current block and next block
        self.putNewBlock()
        self.putNewBlock()
        
    @property
    def width(self):
        return self.__width
    
    # stretch the wall
    def stretch(self, target_width: int)->None:
        # adjust board
        if(self.__width == target_width or target_width < 6):
            return 
        elif(self.__width < target_width):
            for row in range(len(self.__board)):
                if(row < 8 or row >= len(self.__board) - 2): # first eight and last two rows are borders
                    self.__board[row] += (target_width - self.__width) * [-1]
                else: # middle rows
                    self.__board[row] = self.__board[row][:-1] + (target_width - self.__width) * [0] + [-1]
                    for col in range(self.__width + 1, min(len(self.__stretch_board_record[row]), target_width + 1)):  # insert recoreded stretched blocks
                        self.__board[row][col] = self.__stretch_board_record[row][col]                  
        else:        
            for row in range(len(self.__board)):
                self.__stretch_board_record[row] += max(0, (self.__width + 1) - len(self.__stretch_board_record[row])) * [0]
                for col in range(target_width + 1, self.__width + 1): # record the stretched rows
                    self.__stretch_board_record[row][col] = self.__board[row][col]
                if(row < 8 or row >= len(self.__board) - 2): # first eight and last two rows remove border blocks
                    self.__board[row] = self.__board[row][:-(self.__width - target_width)]
                else: # middle rows remove empty blocks
                    self.__board[row] = self.__board[row][:-(self.__width - target_width + 1)] + [-1]
        
        # give value
        self.__width = target_width
 
    # move the block downward by 1 positon if the move is valid. return whether the move is successful
    def tryMoveDown(self)->bool:
        # your code here
        if (self.isBlockValid(self.__cur_block.x, self.__cur_block.y + 1)):
            self.__cur_block.moveDown()
            return True
        return False
    
    # move the block left by 1 positon if the move is valid. return whether the move is successful
    def tryMoveLeft(self)->bool:
        # your code here
        if (self.isBlockValid(self.__cur_block.x - 1, self.__cur_block.y)):
            self.__cur_block.moveLeft()
            return True
        return False
    
    # move the block right by 1 positon if the move is valid. return whether the move is successful
    def tryMoveRight(self)->bool:
        # your code here
        if (self.isBlockValid(self.__cur_block.x + 1, self.__cur_block.y)):
            self.__cur_block.moveRight()
            return True
        return False
    
    # rotate the block counterclockwise by 90 degree if the rotate is valid
    def tryRotateLeft(self)->None:
        self.__cur_block.rotateLeft()
        if(not self.isBlockValid(self.__cur_block.x, self.__cur_block.y)):
            self.__cur_block.rotateRight()
    
    # rotate the block clockwise by 90 degree if the rotate is valid
    def tryRotateRight(self)->None:
        self.__cur_block.rotateRight()
        if(not self.isBlockValid(self.__cur_block.x, self.__cur_block.y)):
            self.__cur_block.rotateLeft()
    
    # write current shape to the board permanently
    def dump(self)->None:
        # your code here
        for i in range(len(self.__cur_block.getShape())):
            for j in range(len(self.__cur_block.getShape()[0])):
                if (self.__cur_block.y + i >= 0 and self.__cur_block.y + i < self.__height and self.__cur_block.x + j < self.__width and self.__cur_block.x + j >= 0): # within the board
                    if(self.__cur_block.getShape()[i][j] == 1):
                        if(self.__cur_block.is_special):
                            self.__board[self.__cur_block.y + 8 + i][self.__cur_block.x + 1 + j] = 3 # special notation '3' for special block
                        else:
                            self.__board[self.__cur_block.y + 8 + i][self.__cur_block.x + 1 + j] = 1 # '1' for normal block

    # put a new block on the top of the board
    def putNewBlock(self)->None:
        # your code here
        self.__cur_block = self.__next_block
        self.__cur_block.x = (self.__width // 2 + 1) - len(self.__cur_block.getShape())
        
        # generate random next block
        rng = random.randint(0, 6)
        if(rng == 0):
            self.__next_block = IBlock(x = self.__width // 2 - 1)
        elif(rng == 1):
            self.__next_block = JBlock(x = self.__width // 2 - 1)
        elif(rng == 2):
            self.__next_block = LBlock(x = self.__width // 2 - 1)
        elif(rng == 3):
            self.__next_block = OBlock(x = self.__width // 2 - 1)
        elif(rng == 4):
            self.__next_block = ZBlock(x = self.__width // 2 - 1)
        elif(rng == 5):
            self.__next_block = TBlock(x = self.__width // 2 - 1)
        elif(rng == 6):
            self.__next_block = SBlock(x = self.__width // 2 - 1)
            
        # randomly give special blocks
        self.__next_block.is_special = random.random() <= self.special_block_rate
        
        # record replay step                 
        self.recordStep()
    
    # check if current block is valid
    def isBlockValid(self, x:int, y:int)->bool:
        # your code here
        for i in range(len(self.__cur_block.getShape())):
            for j in range(len(self.__cur_block.getShape()[0])):
                if(self.__cur_block.getShape()[i][j] == 1):
                    if (y + i >= self.__height or x + j >= self.__width or x + j < 0): # out of three bounds: left, right, bottom
                        return False
                    elif (y + i >= 0 and self.__board[y + 8 + i][x + 1 + j] > 0): # overlaps with other block
                        return False                         
        return True
    
    # the distance of the current block to the wall, 0:UP, 1:LEFT, 2:RIGHT, 3:DOWN
    def distanceToWall(self, direction:int)->int:
        # up
        if(direction == 0):
            return self.__cur_block.y + 1
        
        # left
        elif(direction == 1):
            leftmost_x = len(self.__cur_block.getShape()[0])
            for i in range(len(self.__cur_block.getShape())):
                for j in range(len(self.__cur_block.getShape()[0])):
                    if(self.__cur_block.getShape()[i][j] == 1):
                        leftmost_x = min(leftmost_x, j)
            return leftmost_x + self.__cur_block.x + 1
        
        # right
        elif(direction == 2):
            rightmost_x = 0
            for i in range(len(self.__cur_block.getShape())):
                for j in range(len(self.__cur_block.getShape()[0])):
                    if(self.__cur_block.getShape()[i][j] == 1):
                        rightmost_x = max(rightmost_x, j)
            return self.__width - (rightmost_x + self.__cur_block.x)
        
        # down
        elif(direction == 3):
            return self.__height - self.__cur_block.y
        
        return None
                 
    # detect, color, and remove full rows, return a tuple with the number of blocks need to remove and the special cols set
    def ColorNRemoveFullRows(self, colToRemove: set = None)->tuple[int, set[int]]:
        # detec, color, or remove full rows and special cols
        tmp = [row[:] for row in self.__board]
        specialCol = set()
        numOfRemoveRows = 0
        numOfFullRows = 0
        numOfBlocksDetected = 0
        for row in range(8, 8 + self.__height):
            # remove colored full rows
            if (numOfFullRows == 0):
                if (tmp[row] == [-1] + [4] * (self.__width) + [-1]):
                    numOfRemoveRows += 1
                    self.__board.remove([-1] + [4] * (self.__width) + [-1]) # Remove full rows
                    self.__board.insert(8, [-1] + [0] * (self.__width) + [-1])
                elif (colToRemove != None):
                    for col in colToRemove:
                        self.__board[row][col] = 0 # Remove special cols
            
            # color detected full rows and special column 
            if (numOfRemoveRows == 0):
                isFullrow = True
                for col in range(1, len(tmp[row]) - 1): # detect full rows
                    if(tmp[row][col] == 0):
                        isFullrow = False
                        break
                    if(tmp[row][col] == 3): # detect special blocks
                        specialCol.add(col) 
                if (isFullrow):
                    numOfBlocksDetected += self.__width
                    numOfFullRows += 1
                    self.__board[row] = [-1] + [4] * (self.__width) + [-1] # full rows color
        
        # count special cols blocks            
        if(numOfFullRows > 0):
            for col in specialCol:
                for row in range(8, 8 + self.__height):
                    self.__board[row][col] = 4 # full special columns color 
                numOfBlocksDetected += 1
            numOfBlocksDetected -= len(specialCol) * numOfFullRows
        
        # record steps
        if (numOfRemoveRows > 0 or numOfBlocksDetected > 0):
            self.recordStep()
        
        return (numOfBlocksDetected, specialCol)
    
    # detect loss, if loss return True, else False
    def detectLoss(self)->bool:
        topRow = self.__board[8]
        isLoss = False
        for i in range(len(topRow)):
            if(topRow[i] > 0):
                topRow[i] = -3 # '-3' notation for loss block
                isLoss = True
        if(isLoss):
            self.recordStep()
        return isLoss

    # record the current step
    def recordStep(self)->None:
        self.__records.append(self.getRawBoard())
    
    # get the int-2Dlist board for raw output
    def getRawBoard(self, is_paused: bool = False)->list[list[int]]:
        # deep copy of current board
        tmp = [row[:] for row in self.__board]
        
        # put current block on it
        for i in range(len(self.__cur_block.getShape())):
            for j in range(len(self.__cur_block.getShape()[0])):
                if (self.__cur_block.y + i >= 0 and self.__cur_block.y + i < self.__height and self.__cur_block.x + j < self.__width and self.__cur_block.x + j >= 0): # within the board
                    if(self.__cur_block.getShape()[i][j] == 1):
                        if(self.__cur_block.is_special):
                            tmp[self.__cur_block.y + 8 + i][self.__cur_block.x + 1 + j] = 3 # fall special blocks
                        else:
                            tmp[self.__cur_block.y + 8 + i][self.__cur_block.x + 1 + j] = 2 # fall normal blocks
        
        # show 'P' pattern if paused
        for i in range(4):
            for j in range(4):
                row_index = i + 2
                col_index = self.__width // 2 - 1 + j
                if(is_paused and self.__pause_shape[i][j] == 1): # 'P' pattern
                    tmp[row_index][col_index] = -2 # '-2' notation for pause blocks
                else:
                    tmp[row_index][col_index] = 0 # empty block    
        
        # show previewed next block if not paused
        if(not is_paused):
            start_index_row = int((4 - len(self.__next_block.getShape())) / 2 + 0.5) + 2
            start_index_col = (self.__width // 2 - 3) + start_index_row
            for i in range(len(self.__next_block.getShape())):
                for j in range(len(self.__next_block.getShape()[0])):
                    if(self.__next_block.getShape()[i][j] == 1):
                        if(self.__next_block.is_special):
                            tmp[start_index_row + i][start_index_col + j] = 3 # special block
                        else:
                            tmp[start_index_row + i][start_index_col + j] = 1 # normal block
        return tmp
    
    # get the output of the board
    def getBoard(self, is_paused: bool = False, input: list[list[int]] = None)->str:
        # get input
        if(input == None):
            tmp = self.getRawBoard(is_paused)
        else:
            tmp = input
        
        # transform to string and add colors   
        tmp_string = ''
        for r in range(len(tmp)):
            for c in range(len(tmp[0])):
                if(tmp[r][c] == -3): # pause block
                    tmp_string += Appearance.LOSS_COLOR + Appearance.GAME_BLOCK
                elif(tmp[r][c] == -2): # pause block
                    tmp_string += Appearance.PAUSE_COLOR + Appearance.BORDER_BLOCK
                elif(tmp[r][c] == -1): # border block
                    tmp_string += Appearance.BORDER_COLOR + Appearance.BORDER_BLOCK
                elif(tmp[r][c] == 0): # empty block
                    tmp_string += Appearance.EMPTY_COLOR + Appearance.EMPTY_BLOCK
                elif(tmp[r][c] == 1): # stable block
                    tmp_string += Appearance.STABLE_COLOR + Appearance.GAME_BLOCK
                elif(tmp[r][c] == 2): # falling block
                    tmp_string += Appearance.FALL_COLOR + Appearance.GAME_BLOCK
                elif(tmp[r][c] == 3): # special block
                    tmp_string += Appearance.SPECIAL_COLOR() + Appearance.GAME_BLOCK
                elif(tmp[r][c] == 4): # full row block
                    tmp_string += Appearance.FULLROW_COLOR + Appearance.GAME_BLOCK
            if(r < len(tmp) - 1):
                tmp_string += "\n"
                
        # clean color           
        tmp_string += "\033[0m"
           
        return tmp_string
    
    # get the record based on the given step
    def getRecord(self, step: int = 0)->str:
        self.__current_record_index = min(max(1, self.__current_record_index + step), len(self.__records) - 1)
        tmp_string = self.getBoard(input=self.__records[self.__current_record_index])
           
        return tmp_string
    
    # get the data of the current board
    def getData(self)->dict:
        return {
            "height": self.__height,
            "width": self.__width,
            "boardlst" : self.__board,
            "stretch_board": self.__stretch_board_record,
            "records" : self.__records,
            "current_block_type" : "#" + str(type(self.__cur_block)).split('.')[1][0] if(self.__cur_block.is_special) else str(type(self.__cur_block)).split('.')[1][0],
            "next_block_type" : "#" + str(type(self.__next_block)).split('.')[1][0] if(self.__next_block.is_special) else str(type(self.__next_block)).split('.')[1][0],
        } # '#' notation for special block
    
    # load the data from the given parameters
    def loadData(self, height: int, width: int, board: list[list[int]], stretch_board:list[list[int]], records: list[list[list[int]]], cur_block_type: str, next_block_type: str)->None:
        # read height and width
        self.__height = height
        self.__width = width
        
        # deep copy board, stretch board, and replay records
        self.__board = [row[:] for row in board]
        self.__stretch_board_record = [row[:] for row in stretch_board]
        self.__records = records[:]
        
        # read current block type
        if('I' in cur_block_type):
            self.__cur_block = IBlock(x = self.__width // 2 - 1)
        elif('J' in cur_block_type):
            self.__cur_block = JBlock(x = self.__width // 2 - 1)
        elif('L' in cur_block_type):
            self.__cur_block = LBlock(x = self.__width // 2 - 1)
        elif('O' in cur_block_type):
            self.__cur_block = OBlock(x = self.__width // 2 - 1)
        elif('Z' in cur_block_type):
            self.__cur_block = ZBlock(x = self.__width // 2 - 1)
        elif('T' in cur_block_type):
            self.__cur_block = TBlock(x = self.__width // 2 - 1)
        elif('S' in cur_block_type):
            self.__cur_block = SBlock(x = self.__width // 2 - 1)
        self.__cur_block.is_special = '#' in cur_block_type
        
        # read next block type
        if('I' in next_block_type):
            self.__next_block = IBlock(x = self.__width // 2 - 1)
        elif('J' in next_block_type):
            self.__next_block = JBlock(x = self.__width // 2 - 1)
        elif('L' in next_block_type):
            self.__next_block = LBlock(x = self.__width // 2 - 1)
        elif('O' in next_block_type):
            self.__next_block = OBlock(x = self.__width // 2 - 1)
        elif('Z' in next_block_type):
            self.__next_block = ZBlock(x = self.__width // 2 - 1)
        elif('T' in next_block_type):
            self.__next_block = TBlock(x = self.__width // 2 - 1)
        elif('S' in next_block_type):
            self.__next_block = SBlock(x = self.__width // 2 - 1)
        self.__next_block.is_special = '#' in next_block_type