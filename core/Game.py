from core.Globals import *
from core.Board import Board
from core.KBHit import KBHit
import random
import time
import json
import simpleaudio

class Game:
    is_muted = False
    score_record_high = {
        GameMode.CLASSIC: 0,
        GameMode.STRETCH: 0,
        GameMode.DRAWING: 0
    }
    
    def __init__(self):
        self.board = Board()
        self.kb = KBHit() # a class that read input from the keyboard
        self.game_state = GameState.GAME
        self.game_mode = GameMode.CLASSIC
        self.game_speed = 0 # default is 0
        self.replay_speed = 0.5
        self.score = 0
        
        self.__stretch_width = 20
        self.__tmp_stretch_time = 0
        self.__tmp_start_time = 0
        self.__resume_state = GameState.GAME
        self.__continuous_elimination_times = 0
        self.__music = None
        self.__save = {}

    def run(self)->None:
        '''
        activate the game
        '''
        # ask muted or not
        while(True):
            ismuted = input("Mute audio? (yes / no)\nYour Input: --> ")
            if (ismuted == "yes"):
                Game.is_muted = True
                break
            elif (ismuted == "no"):
                Game.is_muted = False
                break
            print("\033[F\033[K" * 2 + "Please enter correct answer!", end=' ')
        print("\033[F\033[K" * 2, end='')
        
        # main loop
        while(True):
            # main start
            self.start()
            
            # write in save file   
            self.__save["record_high"] = Game.score_record_high
            with open('save.json', 'w') as file:
                json.dump(self.__save, file)
            
            # ask play again
            while(True):
                do_play_again = input("Play again? (yes / no)\nYour Input: --> ")
                if (do_play_again == "yes"):
                    break
                elif (do_play_again == "no"):
                    # Press ANY key to exit
                    print('\033[F\033[KBye! Press ANY key to exit...')
                    while(not self.kb.kbhit()):
                        time.sleep(0.5)
                    return
                print("\033[F\033[K" * 2 + "Please enter correct answer!", end=' ')
            print("\033[F\033[K" * 30, end='')

    def start(self)->None:
        '''
        start the game
        '''
        # initialize
        self.__init__()
        self.__tmp_start_time = time.time()
        
        # read save data
        self.readSave()
        
        # choose mode and difficulty if no save data
        if(self.game_speed == 0):
            self.chooseModeNDifficulty()
        else:
            self.game_state = GameState.PAUSE
            
        # game loop
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
                if(not Game.is_muted):
                    self.__music.stop() # stop the music
                if(self.game_state == GameState.GAME or self.__resume_state == GameState.GAME):
                    self.save() # ask to save the game state
                self.game_state = GameState.NONE # reset gamestate
        
            # pause system
            if(kinput == chr(32)): # SPACE to pause
                self.switchPause()
            
            # game mechanics
            if(self.game_state == GameState.GAME):
                if((not Game.is_muted) and (self.__music == None or not self.__music.is_playing())): # game state music
                    if(self.game_mode == GameMode.CLASSIC):
                        self.__music = self.playAudio(Audio.CLASSIC)
                    elif(self.game_mode == GameMode.STRETCH):
                        self.__music = self.playAudio(Audio.STRETCH)
                    elif(self.game_mode == GameMode.DRAWING):
                        self.__music = self.playAudio(Audio.DRAWING)
                self.update(kinput)
            
            # replay system
            if(self.game_state == GameState.REPLAY):
                if((not Game.is_muted) and (self.__music == None or not self.__music.is_playing())): # replay state music
                    self.__music = self.playAudio(Audio.REPLAY) 
                self.seeReplay(kinput)
            
            # input interval
            time.sleep(0.05)
    
    def chooseModeNDifficulty(self)->None:
        '''
        based on the mode and difficulty chosen, change game mode, the speed of the game, and special block rate
        '''
        # choose game mode
        while(True):
            mode = input("Enter Gamemode: classic, stretch, drawing\nYour Input: --> ")
            if (mode == "classic"):
                self.game_mode = GameMode.CLASSIC
                break
            elif (mode == "stretch"):
                self.game_mode = GameMode.STRETCH
                break
            elif (mode == "drawing"):
                self.game_mode = GameMode.DRAWING
                self.board.is_drawing = True
                self.board.generateDrawings()
                break
            print("\033[F\033[K" * 2 + "Please enter correct gamemode!", end=' ')
        print("\033[F\033[K" * 2, end='')         
        
        # choose game difficulty
        while(True):
            difficulty = input("Enter Difficulty: easy, normal, hard\nYour Input: --> ")
            if (difficulty == "easy"):
                self.game_speed = Difficulty.EASY
                break
            elif (difficulty == "normal"):
                self.game_speed = Difficulty.NORMAL
                break
            elif (difficulty == "hard"):
                self.game_speed = Difficulty.HARD
                break
            print("\033[F\033[K" * 2 + "Please enter correct difficulty!", end=' ')
        self.board.special_block_rate = self.game_speed / 12 + 0.03
        print("\033[F\033[K" * 2, end='')
     
    def stretch(self)->None:
        '''
        stretch the board
        '''
        # cool down time
        if(self.board.width == self.__stretch_width):     
            if(time.time() > self.__tmp_stretch_time + self.game_speed * 5):
                self.__stretch_width = random.randint(6, 30)
                self.__tmp_stretch_time = time.time()
                
        # stretch inside     
        elif(self.board.width > self.__stretch_width):             
            # if being squeezed, then end this block round 
            if(self.board.distanceToWall(2) <= 1 and (not self.board.tryMoveLeft())):
                self.endBlockRound()
            
            # narrow the wall
            self.board.stretch(self.board.width - 1)
            
            # full row event
            self.eliminateEvent()
            
            # reset timer
            self.__tmp_stretch_time = time.time()
            
        # stretch outside
        else:
            # broaden the wall
            self.board.stretch(self.board.width + 1)
            
            # full row event
            self.eliminateEvent()
            
            # reset timer
            self.__tmp_stretch_time = time.time()
            
    def switchPause(self)->None:
        '''
        switch between pause and resume
        '''
        if(self.game_state != GameState.PAUSE):
            self.__resume_state = self.game_state
            self.game_state = GameState.PAUSE
        else:
            self.game_state = self.__resume_state 
            self.__tmp_start_time = time.time()
            self.__tmp_stretch_time = time.time()
            
    def save(self)->None:
        '''
        save current game state
        '''
        # ask save state or not
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
        cur_game_data["mode"] = self.game_mode
        self.__save["saved_game_data"] = cur_game_data
        self.__save["record_high"] = Game.score_record_high
 
        print("\033[F\033[K" * 2, end='Game is saved! ')
    
    def readSave(self)->None:
        '''
        read save file, and clear the data
        '''
        try: 
            with open('save.json', 'r') as file:
                self.__save = json.load(file)
            Game.score_record_high = self.__save["record_high"]
            if(self.__save["saved_game_data"] != {}):
                self.game_speed = self.__save["saved_game_data"]["speed"]
                self.game_mode = self.__save["saved_game_data"]["mode"]
                self.score = self.__save["saved_game_data"]["score"]
                self.board.loadData(self.__save["saved_game_data"]["height"], 
                                    self.__save["saved_game_data"]["width"],
                                    self.__save["saved_game_data"]["boardlst"],
                                    self.__save["saved_game_data"]["stretch_board"],
                                    self.__save["saved_game_data"]["drawing_board"],
                                    self.__save["saved_game_data"]["records"], 
                                    self.__save["saved_game_data"]["current_block_type"], 
                                    self.__save["saved_game_data"]["next_block_type"])
                
                # clear the saved data after read
                self.__save["saved_game_data"] = {} 
                json.dump(self.__save, file)
        except:
            with open('save.json', 'w') as file:
                init_data = {"record_high": {"classic": 0, "stretch": 0, "drawing": 0}, "saved_game_data": {}}
                json.dump(init_data, file)      
               
    def update(self, k_input:str)->None:
        '''
        update all the game mechanics
        '''
        # handle user's inputs
        if (k_input == 'q'):
            if (self.board.tryRotateLeft() and (not Game.is_muted)):
                self.playAudio(Audio.ROTATE) # play rotate audio if not muted
        if (k_input == 'e'):
            if (self.board.tryRotateRight() and (not Game.is_muted)): 
                self.playAudio(Audio.ROTATE) # play rotate audio if not muted
        if (k_input == 'a'):
            self.board.tryMoveLeft()
        if (k_input == 'd'):
            self.board.tryMoveRight()
        if (k_input == 's'): # if 'S' is pressed, drop the block immediately
            while(self.board.tryMoveDown()):
                # Falling animation
                self.display()
                time.sleep(0.015)
            self.endBlockRound()
         
        # game speed cycle
        if(time.time() - self.__tmp_start_time >= self.game_speed):
            # stretch mode: stretch wall
            if(self.game_mode == GameMode.STRETCH):
                self.stretch()
            
            # try movedown
            if(not self.board.tryMoveDown()):
                self.endBlockRound()
            
            # reset start time
            self.__tmp_start_time = time.time()
    
    def endBlockRound(self)->None:
        '''
        end the current block round
        '''
        self.board.dump()
        self.board.putNewBlock()
        
        # play hit audio if not muted
        if (not Game.is_muted):
            self.playAudio(Audio.HIT)
        
        # calculate scores for fallen block
        self.score += round(1 / self.game_speed)
        Game.score_record_high[self.game_mode] = max(Game.score_record_high[self.game_mode], self.score)
        
        # events
        self.eliminateEvent()
        self.lossEvent()   
        
    def eliminateEvent(self)->None:
        '''
        things that will be performed during elimination of blocks
        '''
        detected = self.board.colorDetected() # detect the block units to remove, and color the block units that need to be removed
        
        if(detected == 0):
            self.__continuous_elimination_times = 0
        while(detected > 0):
            self.__continuous_elimination_times += 1
            
            # 0.8s to show the elimination results
            self.display()
            time.sleep(0.8)
            
            # calculate scores for elimination
            self.score += self.__continuous_elimination_times * (detected // self.board.width) * detected
            Game.score_record_high[self.game_mode] = max(Game.score_record_high[self.game_mode], self.score)
            
            # execute elimination
            self.board.removeDetected()

            # update detect
            detected = self.board.colorDetected()
            
        
    def lossEvent(self)->None:
        '''
        things that will be performed after loss
        '''
        if(self.board.detectLoss()):
            # display game final state
            self.display()
            
            # play gameover sound if not muted
            if (not Game.is_muted):
                self.__music.stop()
                self.__music = self.playAudio(Audio.GAMEOVER, is_wait=True)

            # replay text
            print("Game Finish!", end=' ')
            while(True):
                do_see_replay = input("See replay? (yes / no)\nYour Input: --> ")
                if (do_see_replay == "yes"):
                    self.game_state = GameState.REPLAY
                    self.__resume_state = GameState.REPLAY
                    break
                elif (do_see_replay == "no"):
                    self.game_state = GameState.NONE
                    self.__resume_state = GameState.NONE
                    break
                print("\033[F\033[K" * 2 + "Please enter correct answer!", end=' ')
            self.__tmp_start_time = time.time()
            print("\033[F\033[K" * 2, end='') 
    
    def seeReplay(self, k_input:str)->None:
        '''
        review previous round
        '''       
        # Show records
        if(time.time() - self.__tmp_start_time >= self.replay_speed):
            self.__tmp_start_time = time.time()
            self.board.getRecord(1)
        
        # get input
        if (k_input == 'a'): # go backward
            self.board.getRecord(-1)
            self.__tmp_start_time = time.time() + self.replay_speed
        elif (k_input == 'd'): # go forward
            self.board.getRecord(1)
            self.__tmp_start_time = time.time() + self.replay_speed
                 
    def display(self)->None:
        '''
        print board on the command line
        '''
        if(self.game_state == GameState.GAME):
            print("\033[F\033[K" * 28 + f"You are gaming in mode {self.game_mode}!\nYour Scores: {self.score}, Your Record: {Game.score_record_high[self.game_mode]}\n" + self.board.getBoard() + f"\nControl: Press 'SPACE' to pause the game, 'ESC' to quit the game...", flush=True) # "\033[F\033[K" * 19 means clear the previous linse of output to avoid jittering
        if(self.game_state == GameState.REPLAY):
            print("\033[F\033[K" * 28 + f"You are watching replay!\nYour Scores: {self.score}, Your Record: {Game.score_record_high[self.game_mode]}\n" + self.board.getRecord() + "\nControl: Press 'D' to go forward, 'A' to go backward, 'SPACE' to pause the game, 'ESC' to quit the replay...", flush=True)
        if(self.game_state == GameState.PAUSE):
            if(self.__resume_state == GameState.GAME):
                print("\033[F\033[K" * 28 + f"You are pausing in mode {self.game_mode}!\nYour Scores: {self.score}, Your Record: {Game.score_record_high[self.game_mode]}\n" + self.board.getBoard(is_paused=True) + "\nControl: Press 'SPACE' to resume the game, 'ESC' to quit the game...", flush=True)
            if(self.__resume_state == GameState.REPLAY):
                print("\033[F\033[K" * 28 + f"You are pausing in replay!\nYour Scores: {self.score}, Your Record: {Game.score_record_high[self.game_mode]}\n" + self.board.getRecord() + "\nControl: Press 'SPACE' to resume the game, 'ESC' to quit the game...", flush=True)
                
    def playAudio(self, wave_obj:str, is_wait: bool = False)->simpleaudio.PlayObject:
        '''
        play the audio based on the input wave object, return the play object, and if is_wait, block until the audio finish
        '''   
        # read and play the audio from file path
        try:
            play_obj = wave_obj.play()
        except:
            pass
         
        # if wait, block until the audio finish
        if(is_wait):
            play_obj.wait_done()
            return None
        
        return play_obj