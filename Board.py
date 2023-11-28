from Block import *
import random
import time

class Board:
    def __init__(self):
        self.__cur_block = BaseBlock()
        self.__next_block = BaseBlock()
        self.__board = [["\u25A0"] * 20 for _ in range(15)]
        self.__records = []
        self.__current_record_index = 1 
        self.__pause_shape = \
            [["\u25A3", "\u25A3", "\u25A3", "\u25A3"],
             ["\u25A3", "\u25A0", "\u25A0", "\u25A3"],
             ["\u25A3", "\u25A3", "\u25A3", "\u25A3"],
             ["\u25A3", "\u25A0", "\u25A0", "\u25A0"]]
        
        # twice to generate random for both current block and next block
        self.putNewBlock()
        self.putNewBlock()
    
    # check if current block is valid
    def isBlockValid(self, x:int, y:int)->bool:
        # your code here
        for i in range(len(self.__cur_block.getShape())):
            for j in range(len(self.__cur_block.getShape()[0])):
                if(self.__cur_block.getShape()[i][j] == "\u25A3"):
                    if (y + i >= 15 or x + j >= 20 or x + j < 0): # out of three bounds: left, right, bottom
                        return False
                    elif (y + i >= 0 and "\u25A3" in self.__board[y + i][x + j]): # overlaps with other block
                        return False
                                 
        return True
    
    # move the block downward by 1 positon if the move is valid, otherwise do nothing. return whether the move is successful
    def tryMoveDown(self)->bool:
        # your code here
        if (self.isBlockValid(self.__cur_block.x, self.__cur_block.y + 1)):
            self.__cur_block.moveDown()
            return True
        return False
    
    # move the block left by 1 positon if the move is valid, otherwise do nothing 
    def tryMoveLeft(self)->None:
        # your code here
        if (self.isBlockValid(self.__cur_block.x - 1, self.__cur_block.y)):
            self.__cur_block.moveLeft()
    
    # move the block right by 1 positon if the move is valid, otherwise do nothing 
    def tryMoveRight(self)->None:
        # your code here
        if (self.isBlockValid(self.__cur_block.x + 1, self.__cur_block.y)):
            self.__cur_block.moveRight()
    
    # rotate the block counterclockwise by 90 degree if the rotate is valid, otherwise do nothing
    def tryRotateLeft(self)->None:
        self.__cur_block.rotateLeft()
        if(not self.isBlockValid(self.__cur_block.x, self.__cur_block.y)):
            self.__cur_block.rotateRight()
    
    # rotate the block clockwise by 90 degree if the rotate is valid, otherwise do nothing
    def tryRotateRight(self)->None:
        self.__cur_block.rotateRight()
        if(not self.isBlockValid(self.__cur_block.x, self.__cur_block.y)):
            self.__cur_block.rotateLeft()
    
    # write current shape to the board permanently
    def dump(self)->None:
        # your code here
        for i in range(len(self.__cur_block.getShape())):
            for j in range(len(self.__cur_block.getShape()[0])):
                if (self.__cur_block.y + i >= 0 and self.__cur_block.y + i < 15 and self.__cur_block.x + j < 20 and self.__cur_block.x + j >= 0): # within the board
                    if(self.__cur_block.getShape()[i][j] == "\u25A3"):
                        self.__board[self.__cur_block.y + i][self.__cur_block.x + j] = "\033[93m\u25A3\033[0m" # Yellow block

    # put a new block on the top of the board
    def putNewBlock(self)->None:
        # your code here
        self.__cur_block = self.__next_block
        self.__cur_block.x = 11 - len(self.__cur_block.getShape())
        
        # generate random next block
        rng = random.randint(0, 6)
        if(rng == 0):
            self.__next_block = IBlock()
        if(rng == 1):
            self.__next_block = JBlock()
        if(rng == 2):
            self.__next_block = LBlock()
        if(rng == 3):
            self.__next_block = OBlock()
        if(rng == 4):
            self.__next_block = ZBlock()
        if(rng == 5):
            self.__next_block = TBlock()
        if(rng == 6):
            self.__next_block = SBlock()
                             
        self.recordStep()
    
    # record the current step
    def recordStep(self)->None:
        self.__records.append(self.toString())
        
    # detect, color, and remove full rows, return the number of full rows
    def ColorNRemoveFullRows(self)->int:
        tmp = [self.__board[i][:] for i in range(15)]
        
        # remove colored full rows
        hasRemoveRows = 0
        for row in tmp:
            if (row == ["\033[92m\u25A3\033[0m"] * 20):
                hasRemoveRows += 1
                self.__board.remove(["\033[92m\u25A3\033[0m"] * 20) # Remove full rows
                self.__board.insert(0, ["\u25A0"] * 20)  

        # color detected full rows
        hasFullRows = 0
        for row in range(len(tmp)):
            if (tmp[row] == ["\033[93m\u25A3\033[0m"] * 20):
                hasFullRows += 1
                self.__board[row] = ["\033[92m\u25A3\033[0m"] * 20 # Add green color
        
        # record steps
        if (hasRemoveRows > 0 or hasFullRows > 0):
            self.recordStep()
        
        return hasRemoveRows + hasFullRows
    
    # detect loss, if loss return True, else False
    def detectLoss(self)->bool:
        topRow = self.__board[0]
        isLoss = False
        for i in range(len(topRow)):
            if(topRow[i] == "\033[93m\u25A3\033[0m"):
                isLoss = True
                topRow[i] = "\033[95m\u25A3\033[0m"
        if(isLoss):
            self.recordStep()
        return isLoss
    
    # return the current board with block on it 
    def toString(self, is_paused: bool = False)->str:
        # deep copy
        tmp = [self.__board[i][:] for i in range(15)]
        
        # put current block on it
        for i in range(len(self.__cur_block.getShape())):
            for j in range(len(self.__cur_block.getShape()[0])):
                if (self.__cur_block.y + i >= 0 and self.__cur_block.y + i < 15 and self.__cur_block.x + j < 20 and self.__cur_block.x + j >= 0): # within the board
                    if(self.__cur_block.getShape()[i][j] == "\u25A3"):
                        tmp[self.__cur_block.y + i][self.__cur_block.x + j] = '\033[94m\u25A3\033[0m' # blue blocks
        
        # put next block on it if not paused, else put a purple 'P' pattern on it
        for i in range(2):
            tmp.insert(0, ['\033[38;5;22m\u2588\033[0m'] * 20)
        for i in range(4):
            tmp.insert(0, ['\033[38;5;22m\u2588\033[0m'] * 8 + ['\u25A0'] * 4 + ['\033[38;5;22m\u2588\033[0m'] * 8)
        if (is_paused):
            for i in range(4):
                for j in range(4):
                    if(self.__pause_shape[i][j] == "\u25A3"):
                        tmp[i][8 + j] = "\033[35m\u2588\033[0m" # purple 'P' pattern
        else:
            start_index_row = (4 - len(self.__next_block.getShape())) // 2
            start_index_col = 8 + start_index_row
            for i in range(len(self.__next_block.getShape())):
                for j in range(len(self.__next_block.getShape()[0])):
                    if(self.__next_block.getShape()[i][j] == "\u25A3"):
                        tmp[start_index_row + i][start_index_col + j] = "\033[93m\u25A3\033[0m"
        
        # transform to string and add borders     
        tmp_string = ''
        for r in range(len(tmp)):
            tmp_string += '\033[38;5;22m\u2588\033[0m' # red borders
            for c in range(len(tmp[0])):
                tmp_string += "\033[38;2;40;40;40m" + tmp[r][c]
            tmp_string += '\033[38;5;22m\u2588\033[0m\n' # red borders
           
        return '\033[38;5;22m' + '\u2588' * 22 + '\n' + '\u2588' * 22 + '\n' + '\033[0m' + tmp_string + '\033[38;5;22m' + '\u2588' * 22 + '\n' + '\u2588' * 22 + '\033[0m'
    
    # get the record based on the given step
    def getRecord(self, step: int = 0)->str:
        self.__current_record_index = min(max(1, self.__current_record_index + step), len(self.__records) - 1)
        return self.__records[self.__current_record_index]
    
    # get the data of the current board
    def getData(self)->dict:
        return {
            "boardlst" : self.__board,
            "records" : self.__records,
            "current_block_type" : str(type(self.__cur_block)).split('.')[1][0],
            "next_block_type" : str(type(self.__next_block)).split('.')[1][0],
        }
    
    # load the data from the given parameters
    def loadData(self, board: list[list[str]], records: list[str], cur_block_type: str, next_block_type: str)->None:
        # deep copy board and replay records
        self.__board = [board[i][:] for i in range(15)]
        self.__records = records[:]
        
        # read current block type
        if(cur_block_type == 'I'):
            self.__cur_block = IBlock()
        if(cur_block_type == 'J'):
            self.__cur_block = JBlock()
        if(cur_block_type == 'L'):
            self.__cur_block = LBlock()
        if(cur_block_type == 'O'):
            self.__cur_block = OBlock()
        if(cur_block_type == 'Z'):
            self.__cur_block = ZBlock()
        if(cur_block_type == 'T'):
            self.__cur_block = TBlock()
        if(cur_block_type == 'S'):
            self.__cur_block = SBlock()
        
        # read next block type
        if(next_block_type == 'I'):
            self.__next_block = IBlock()
        if(next_block_type == 'J'):
            self.__next_block = JBlock()
        if(next_block_type == 'L'):
            self.__next_block = LBlock()
        if(next_block_type == 'O'):
            self.__next_block = OBlock()
        if(next_block_type == 'Z'):
            self.__next_block = ZBlock()
        if(next_block_type == 'T'):
            self.__next_block = TBlock()
        if(next_block_type == 'S'):
            self.__next_block = SBlock()