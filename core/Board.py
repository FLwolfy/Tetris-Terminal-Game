from core.Globals import *
from core.Block import *
import random

class Board:
    def __init__(self, height: int = 15, width : int = 20, special_block_rate: float = 0):
        self.special_block_rate = special_block_rate
        self.is_drawing = False
        
        self.__height = height
        self.__width = width
        self.__cur_block = BaseBlock()
        self.__next_block = BaseBlock()
        self.__board = [[-1] * (self.__width + 2) for _ in range(8)] + \
                       [[-1] + [0] * (self.__width) + [-1] for _ in range(self.__height)] + \
                       [[-1] * (self.__width + 2) for _ in range(2)]
        self.__stretch_board_record = [[-1] + [0] * (self.__width + 1) for _ in range(self.__height + 10)]
        self.__is_drawing_matched = False
        self.__drawings_shapes = shapes = \
            [
            [[0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [1, 1, 1, 0]],
            
            [[0, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 1]],
            
            [[0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [1, 1, 0, 0]],
            
            [[0, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1]],
            
            [[0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [1, 1, 1, 0]],
            
            [[0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [1, 1, 1, 0]],
            
            [[0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0]],
            
            [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 0, 0, 1]],
            
            [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 1],
            [1, 1, 1, 1]],
            
            [[0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0]],
            
            [[1, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 1]],
            
            [[1, 1, 1, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]],
            
            [[0, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0]],
            
            [[0, 1, 1, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0]],
            
            [[1, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0]],
            
            [[0, 1, 1, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0]],
            
            [[1, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0]],
            
            [[0, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 1, 0],
            [0, 1, 1, 1]],
            
            [[0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 0]],
            ]
        self.__drawings_board = \
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]] # has to be 4*4
        self.__pause_shape = \
            [[1, 1, 1, 1],
             [1, 0, 0, 1],
             [1, 1, 1, 1],
             [1, 0, 0, 0]] # has to be 4*4
        self.__records = []
        self.__current_record_index = 1 
        
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
                # first eight and last two rows are borders
                if(row < 8 or row >= len(self.__board) - 2):
                    self.__board[row] += (target_width - self.__width) * [-1]
                    
                # middle rows
                else:
                    self.__board[row] = self.__board[row][:-1] + (target_width - self.__width) * [0] + [-1]
                    
                    # insert recoreded stretched blocks
                    for col in range(self.__width + 1, min(len(self.__stretch_board_record[row]), target_width + 1)):
                        self.__board[row][col] = self.__stretch_board_record[row][col]                  
        else:        
            for row in range(len(self.__board)):
                self.__stretch_board_record[row] += max(0, (self.__width + 1) - len(self.__stretch_board_record[row])) * [0]
                
                # record the stretched rows
                for col in range(target_width + 1, self.__width + 1): 
                    self.__stretch_board_record[row][col] = self.__board[row][col]
                    
                # first eight and last two rows remove border blocks
                if(row < 8 or row >= len(self.__board) - 2): 
                    self.__board[row] = self.__board[row][:-(self.__width - target_width)]
                    
                # middle rows remove empty blocks
                else:
                    self.__board[row] = self.__board[row][:-(self.__width - target_width + 1)] + [-1]
        
        # set value
        self.__width = target_width
        
    # generate drawings on board
    def generateDrawings(self)->None:
        # generate random drawings
        index = random.randint(0,len(self.__drawings_shapes) - 1)
        self.__drawings_board = self.__drawings_shapes[index]
 
    # move the block downward by 1 positon if the move is valid. return whether the move is successful
    def tryMoveDown(self)->bool:
        if (self.isBlockValid(self.__cur_block.x, self.__cur_block.y + 1)):
            self.__cur_block.moveDown()
            return True
        return False
    
    # move the block left by 1 positon if the move is valid. return whether the move is successful
    def tryMoveLeft(self)->bool:
        if (self.isBlockValid(self.__cur_block.x - 1, self.__cur_block.y)):
            self.__cur_block.moveLeft()
            return True
        return False
    
    # move the block right by 1 positon if the move is valid. return whether the move is successful
    def tryMoveRight(self)->bool:
        if (self.isBlockValid(self.__cur_block.x + 1, self.__cur_block.y)):
            self.__cur_block.moveRight()
            return True
        return False
    
    # rotate the block counterclockwise by 90 degree if the rotate is valid. return whether the move is successful
    def tryRotateLeft(self)->bool:
        self.__cur_block.rotateLeft()
        if(not self.isBlockValid(self.__cur_block.x, self.__cur_block.y)):
            self.__cur_block.rotateRight()
            return False
        return True
    
    # rotate the block clockwise by 90 degree if the rotate is valid. return whether the move is successful
    def tryRotateRight(self)->bool:
        self.__cur_block.rotateRight()
        if(not self.isBlockValid(self.__cur_block.x, self.__cur_block.y)):
            self.__cur_block.rotateLeft()
            return False
        return True
    
    # write current shape to the board permanently
    def dump(self)->None:
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
        self.__cur_block = self.__next_block
        self.__cur_block.x = (self.__width // 2 + 1) - len(self.__cur_block.getShape())
        self.__cur_block.y = -len(self.__cur_block.getShape())
        
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
        for i in range(len(self.__cur_block.getShape())):
            for j in range(len(self.__cur_block.getShape()[0])):
                if(self.__cur_block.getShape()[i][j] == 1):
                    # out of three bounds: left, right, bottom
                    if (y + i >= self.__height or x + j >= self.__width or x + j < 0): 
                        return False
                    
                    # overlaps with other block
                    elif (y + i >= 0 and self.__board[y + 8 + i][x + 1 + j] > 0): 
                        return False                         
        return True
                 
    # color the detected units, return the number of blocks colored
    def colorDetected(self)->int:
        num_of_blocks_detected = 0
        full_rows, special_cols = self.detectFullRowsNSpecialCols()
        
        # color the units that match the drawing
        if(self.is_drawing):
            match_pos = self.detectDrawings()
            if(match_pos != None):
                self.__is_drawing_matched = True
                # color matched drawing block units
                for i in range(4):
                    for j in range(4):
                        if(self.__drawings_board[i][j] == 1):
                            if(self.__board[match_pos[0] + 8 + i][match_pos[1] + 1 + j] == 3):
                                special_cols.add(match_pos[1] + j)
                            self.__board[match_pos[0] + 8 + i][match_pos[1] + 1 + j] = -4 
                            num_of_blocks_detected += 1
                
                # color explode block units
                tmp = [row[1:-1] for row in self.__board[8:-2]] # deep copy
                for y in range(match_pos[0] - 3, match_pos[0] + 7):
                    for x in range(match_pos[1] - 3, match_pos[1] + 7):
                        if (y < 0 or y >= self.__height or x >= self.__width or x < 0): # out of boundaries
                            continue
                        if (not (y < match_pos[0] or y >= match_pos[0] + 4 or x >= match_pos[1] + 4 or x < match_pos[1])): # inside drawings
                            continue
                        for i, j in ((match_pos[0] + 1, match_pos[1] + 1), 
                                    (match_pos[0] + 2, match_pos[1] + 1), 
                                    (match_pos[0] + 1, match_pos[1] + 2), 
                                    (match_pos[0] + 2, match_pos[1] + 2)):
                            if(abs(y - i) + abs(x - j) <= 5):
                                if(tmp[y][x] == 3):
                                    special_cols.add(x)
                                self.__board[y + 8][x + 1] = 5 # explode color
                                if(tmp[y][x] > 0):
                                    num_of_blocks_detected += 1
                                                     
        # color full rows and special cols detected
        for row in range(self.__height):  
            # color full row
            if (row in full_rows):
                num_of_blocks_detected += self.__width
                self.__board[row + 8] = [-1] + [4] * (self.__width) + [-1]
                
            # color full special columns
            for col in special_cols:
                if(self.__board[row + 8][col + 1] != -4 and self.__board[row + 8][col + 1] != 5): # not drawing blocks and explode blocks
                    self.__board[row + 8][col + 1] = 4
                    num_of_blocks_detected += 1
        num_of_blocks_detected -= len(special_cols) * len(full_rows)
        
        # record replay steps
        if (num_of_blocks_detected > 0):
            self.recordStep()
        
        return num_of_blocks_detected
    
    # remove the detected units that have been colored
    def removeDetected(self)->None:
        has_removed = False
        
        # remove full rows
        for row in range(self.__height):
            if(self.__board[row + 8] == [-1] + [4] * self.__width + [-1]):
                self.__board.remove([-1] + [4] * self.__width + [-1])
                self.__board.insert(8, [-1] + [0] * self.__width + [-1])  
        
        # remove special col and detected drawings      
        for row in range(self.__height):
            for col in range(self.__width):
                if(self.__board[row + 8][col + 1] == 4 or self.__board[row + 8][col + 1] == -4 or self.__board[row + 8][col + 1] == 5): # detected, drawing, and explode blocks
                    self.__board[row + 8][col + 1] = 0 # empty block unit
                    has_removed = True
        
        # generate new drawings
        if(self.__is_drawing_matched):
            self.generateDrawings()
            self.__is_drawing_matched = False
        
        # record steps if remove
        if (has_removed):
            self.recordStep()
    
    # record the current step for replay
    def recordStep(self)->None:
        self.__records.append(self.getRawBoard())
    
    # detect if there are full rows and special cols, return the tuple of full rows and special cols  
    def detectFullRowsNSpecialCols(self)->tuple[set,set]:
        full_rows = set()
        special_cols = set()
        current_cols = set()
        
        # detect full rows and special cols
        for row in range(self.__height):
            isFullrow = True
            current_cols.clear()
            for col in range(self.__width):       
                # detect full rows
                if(self.__board[row + 8][col + 1] == 0):
                    isFullrow = False
                    break
                
                # detect special blocks
                if(self.__board[row + 8][col + 1] == 3):
                    current_cols.add(col)
                    
            if(isFullrow):
                full_rows.add(row)
                special_cols.update(current_cols)
        
        # return the tuple of full rows and special cols
        return (full_rows, special_cols)
            
    # detect if the drawing has been matched, return the lefttop position if matched, elss return None
    def detectDrawings(self)->tuple[int,int]:
        for row in range(self.__height - 3):
            for col in range(self.__width - 3):
                is_matched = True
                for i in range(4):
                    for j in range(4):
                        if(self.__drawings_board[i][j] == 1 and self.__board[row + 8 + i][col + 1 + j] == 0):
                            is_matched = False
                        elif(self.__drawings_board[i][j] == 0 and self.__board[row + 8 + i][col + 1 + j] != 0):
                            is_matched = False
                if(is_matched):
                    return (row, col)
        return None
    
    # detect loss, if loss return True, else False
    def detectLoss(self)->bool:
        top_row = self.__board[8]
        is_loss = False
        for i in range(len(top_row)):
            if(top_row[i] > 0):
                top_row[i] = -3 # '-3' notation for loss block
                is_loss = True
        if(is_loss):
            self.recordStep()
        return is_loss
    
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
    
    # get the 2Dlist[int] board for raw output
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
                        
        # show the drawings block
        if(self.is_drawing and not is_paused):
            for i in range(4):
                for j in range(4):
                    row_index = i + 2
                    col_index = self.__width // 2 - 1 + j
                    if(self.__drawings_board[i][j] == 1):
                        tmp[row_index][col_index] = -4 # '-4' notation for drawing blocks
                    else:
                        tmp[row_index][col_index] = 0 # empty block              
        
        # show previewed next block if not paused
        elif(not is_paused):
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
                if(tmp[r][c] == -4): # drawing block
                    tmp_string += Appearance.DRAWING_COLOR + Appearance.DRAWING_BLOCK
                elif(tmp[r][c] == -3): # loss block
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
                elif(tmp[r][c] == 4): # detected block
                    tmp_string += Appearance.DETECTED_COLOR + Appearance.GAME_BLOCK
                elif(tmp[r][c] == 5): # explode block
                    tmp_string += Appearance.EXPLODE_COLOR + Appearance.GAME_BLOCK
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
            "drawing_board": self.__drawings_board,
            "records" : self.__records,
            "current_block_type" : "#" + str(type(self.__cur_block)).split('Block.')[1][0] if(self.__cur_block.is_special) else str(type(self.__cur_block)).split('Block.')[1][0],
            "next_block_type" : "#" + str(type(self.__next_block)).split('Block.')[1][0] if(self.__next_block.is_special) else str(type(self.__next_block)).split('Block.')[1][0],
        } # '#' notation for special block
    
    # load the data from the given parameters
    def loadData(self, height: int, width: int, board: list[list[int]], stretch_board:list[list[int]], drawing_board:list[list[int]], records: list[list[list[int]]], cur_block_type: str, next_block_type: str)->None:
        # read height and width
        self.__height = height
        self.__width = width
        
        # deep copy board, stretch board, drawing board, and replay records
        self.__board = [row[:] for row in board]
        self.__stretch_board_record = [row[:] for row in stretch_board]
        self.__drawings_board = [row[:] for row in drawing_board]
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
