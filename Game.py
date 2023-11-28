from Board import Board
from KBHit import KBHit
import time
import json

class GameState:
    NONE = 0
    GAME = 1
    REPLAY = 2
    PAUSE = 3

class Game:
    score_record_high = 0
    
    def __init__(self):
        self.board = Board()
        self.kb = KBHit() # a class that read input from the keyboard
        self.game_state = GameState.NONE
        self.game_speed = 0 # the larger, the slower
        self.replay_speed = 0.5
        self.tmp_start_time = 0
        self.score = 0
        
        self.__resume_state = GameState.NONE
        self.__detected_full_rows_times = 0
        
        # read save file
        try: 
            with open('save.json', 'r') as file:
                self.__save = json.load(file)
            Game.score_record_high = self.__save["record_high"]
            if(self.__save["saved_game_data"] != {}):
                self.game_speed = self.__save["saved_game_data"]["speed"]
                self.score = self.__save["saved_game_data"]["score"]
                self.board.loadData(self.__save["saved_game_data"]["boardlst"], self.__save["saved_game_data"]["records"], self.__save["saved_game_data"]["current_block_type"], self.__save["saved_game_data"]["next_block_type"])
                self.__save["saved_game_data"] = {} # clear the saved data after read
        except:
            with open('save.json', 'w') as file:
                init_data = {"record_high": 0, "saved_game_data": {}}
                json.dump(init_data, file)

    # activate the game
    def run(self)->None:
        while(True):
            # main start
            self.start()
            
            # write in save file
            self.__save["record_high"] = Game.score_record_high
            with open('save.json', 'w') as file:
                json.dump(self.__save, file)
            
            # ask play again
            while(True):
                doPlayAgain = input("Play again? (yes / no)\nYour Input: --> ")
                if (doPlayAgain == "yes"):
                    break
                elif (doPlayAgain == "no"):
                    # Press ANY key to exit
                    print('\033[F\033[KBye! Press ANY key to exit...')
                    while(not self.kb.kbhit()):
                        time.sleep(0.5)
                    return
                print("\033[F\033[K" * 2 + "Please enter correct answer!", end=' ')
            print("\033[F\033[K" * 30, end='')

    # start the game
    def start(self)->None:
        # initialize
        self.__init__()
        self.tmp_start_time = time.time()
        self.game_state = GameState.GAME
        self.__resume_state = GameState.GAME
        
        # choose difficulty if no save data
        if(self.game_speed == 0):
            self.chooseDifficulty()
        else:
            self.game_state = GameState.PAUSE
            
        # main game loop
        print('\n' * 27)
        while(self.game_state != GameState.NONE):
            # get input
            kinput = ''         
            if self.kb.kbhit():
                while self.kb.kbhit(): # only get the most recent input
                    try:
                        kinput = self.kb.getch()
                    except:
                        pass
                self.kb.set_normal_term()
                
            # update board
            self.display()
            
            # exit system
            if (kinput == chr(27)): # ESC to exit
                if(self.game_state == GameState.GAME or self.__resume_state == GameState.GAME):
                    self.save() # ask to save the game state   
                self.game_state = GameState.NONE
        
            # pause system
            if(kinput == chr(32)): # SPACE to pause
                self.switchPause()
            
            # game mechanics
            if(self.game_state == GameState.GAME):
                self.update(kinput)
            
            # replay system
            if(self.game_state == GameState.REPLAY):
                self.seeReplay(kinput)
            
            # input interval
            time.sleep(0.05)
    
    # based on the difficulty chosen, change the speed of the game      
    def chooseDifficulty(self)->None:
        while(True):
            difficulty = input("Enter Difficulty: easy, normal, hard\nYour Input: --> ")
            if (difficulty == "easy"):
                self.game_speed = 0.8
                break
            elif (difficulty == "normal"):
                self.game_speed = 0.4
                break
            elif (difficulty == "hard"):
                self.game_speed = 0.2
                break
            print("\033[F\033[K" * 2 + "Please enter correct difficulty!", end=' ')
        print("\033[F\033[K" * 2, end='')
            
    # switch between pause and resume
    def switchPause(self)->None:
        if(self.game_state != GameState.PAUSE):
            self.__resume_state = self.game_state
            self.game_state = GameState.PAUSE
        else:
            self.game_state = self.__resume_state 
            
    # save current game state
    def save(self)->None:
        # ask save of not
        while(True):
            doSave = input("Save current state? (yes / no)\nYour Input: --> ")
            if (doSave == "yes"):
                break
            elif (doSave == "no"):
                print("\033[F\033[K" * 2, end='')
                return
            print("\033[F\033[K" * 2 + "Please enter correct answer!", end=' ')
            
        # save board, block types, difficulty, replay records and scores
        cur_game_data = self.board.getData()
        cur_game_data["score"] = self.score
        cur_game_data["speed"] = self.game_speed 
        self.__save["saved_game_data"] = cur_game_data
 
        print("\033[F\033[K" * 2, end='Game is saved! ')
        
               
    # update all the game mechanics
    def update(self, kinput:str)->None:
        # end the current block round
        def endBlockRound(self: Game)->None:
            self.board.dump()
            self.board.putNewBlock()
            
            # calculate scores for fallen block
            self.score += round(1 / self.game_speed)
            Game.score_record_high = max(Game.score_record_high, self.score)
            
            # Detect Full rows
            numOfFullRows = self.board.ColorNRemoveFullRows() # detect and color the full rows
            if(numOfFullRows > 0):
                self.__detected_full_rows_times += 1
                
                # 0.5s to show the full rows
                self.display()
                time.sleep(0.5)
                
                # calculate scores for full rows
                self.score += self.__detected_full_rows_times * numOfFullRows * 20
                Game.score_record_high = max(Game.score_record_high, self.score)
                
                # Remove full rows
                self.board.ColorNRemoveFullRows()
            else:
                self.__detected_full_rows_times = 0
            
            # Detect loss
            if(self.board.detectLoss()):
                # display game final state
                self.display()
    
                # replay text
                print("Game Finish!", end=' ')
                while(True):
                    doSeeReplay = input("See replay? (yes / no)\nYour Input: --> ")
                    if (doSeeReplay == "yes"):
                        self.game_state = GameState.REPLAY
                        self.__resume_state = GameState.REPLAY
                        break
                    elif (doSeeReplay == "no"):
                        self.game_state = GameState.NONE
                        self.__resume_state = GameState.NONE
                        break
                    print("\033[F\033[K" * 2 + "Please enter correct answer!", end=' ')
                self.tmp_start_time = time.time()
                print("\033[F\033[K" * 2, end='')
                
        # handle user's inputs
        if (kinput == 'q'):
            self.board.tryRotateLeft()
        if (kinput == 'e'):
            self.board.tryRotateRight()
        if (kinput == 'a'):
            self.board.tryMoveLeft()
        if (kinput == 'd'):
            self.board.tryMoveRight()
        if (kinput == 's'): # if 'S' is pressed, drop the block immediately
            while(self.board.tryMoveDown()):
                # Falling animation
                self.display()
                time.sleep(0.015)
            endBlockRound(self)
         
        # move down if possible, otherwise end the current block round
        if(time.time() - self.tmp_start_time >= self.game_speed):
            self.tmp_start_time = time.time()
            if(not self.board.tryMoveDown()):
                endBlockRound(self)
    
    # review previous round
    def seeReplay(self, kinput:str)->None:
        
        # Show records
        if(time.time() - self.tmp_start_time >= self.replay_speed):
            self.tmp_start_time = time.time()
            self.board.getRecord(1)
        
        # get input
        if (kinput == 'a'): # go backward
            self.board.getRecord(-1)
            self.tmp_start_time = time.time() + self.replay_speed
        elif (kinput == 'd'): # go forward
            self.board.getRecord(1)
            self.tmp_start_time = time.time() + self.replay_speed
                 
    # print board on the command line
    def display(self)->None:
        # your code here
        if(self.game_state == GameState.GAME):
            print("\033[F\033[K" * 28 + f"You are gaming!\nYour Scores: {self.score}, Your Record: {Game.score_record_high}\n" + self.board.toString() + f"\nControl: Press 'SPACE' to pause the game, 'ESC' to quit the game...", flush=True) # "\033[F\033[K" * 19 means clear the previous output to avoid jittering
        if(self.game_state == GameState.REPLAY):
            print("\033[F\033[K" * 28 + f"You are watching replay!\nYour Scores: {self.score}, Your Record: {Game.score_record_high}\n" + self.board.getRecord() + "\nControl: Press 'D' to go forward, 'A' to go backward, 'SPACE' to pause the game, 'ESC' to quit the replay...", flush=True)
        if(self.game_state == GameState.PAUSE):
            if(self.__resume_state == GameState.GAME):
                print("\033[F\033[K" * 28 + f"You are pausing!\nYour Scores: {self.score}, Your Record: {Game.score_record_high}\n" + self.board.toString(is_paused=True) + "\nControl: Press 'SPACE' to resume the game, 'ESC' to quit the game...", flush=True) # "\033[F\033[K" * 19 means clear the previous output to avoid jittering
            if(self.__resume_state == GameState.REPLAY):
                print("\033[F\033[K" * 28 + f"You are pausing!\nYour Scores: {self.score}, Your Record: {Game.score_record_high}\n" + self.board.getRecord() + "\nControl: Press 'SPACE' to resume the game, 'ESC' to quit the game...", flush=True)
