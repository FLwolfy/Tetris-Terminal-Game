import simpleaudio
import time

class Audio:
    # audio path
    CLASSIC = simpleaudio.WaveObject.from_wave_file("audio/classic.wav")
    STRETCH = simpleaudio.WaveObject.from_wave_file("audio/stretch.wav")
    DRAWING = simpleaudio.WaveObject.from_wave_file("audio/drawing.wav")
    GAMEOVER = simpleaudio.WaveObject.from_wave_file("audio/gameover.wav")
    HIT = simpleaudio.WaveObject.from_wave_file("audio/hit.wav")
    REPLAY = simpleaudio.WaveObject.from_wave_file("audio/replay.wav")
    ROTATE = simpleaudio.WaveObject.from_wave_file("audio/rotate.wav")

class Difficulty:
    # block fall frequency
    HARD = 0.2
    NORMAL = 0.4
    EASY = 0.7

class GameState:
    # enum for gamestate
    NONE = 0
    GAME = 1
    REPLAY = 2
    PAUSE = 3
    
class GameMode:
    # enum for gamemode
    CLASSIC = "classic"
    STRETCH = "stretch"
    DRAWING = "drawing"
    
class Appearance:
    # block units
    EMPTY_BLOCK = "\u25A0"
    GAME_BLOCK = "\u25A3"
    BORDER_BLOCK = "\u2588"
    DRAWING_BLOCK = "\u25A7"
    
    # colors
    EMPTY_COLOR = "\033[38;2;40;40;40m" # gray
    BORDER_COLOR = "\033[38;5;22m" # red
    PAUSE_COLOR = "\033[35m" # light purple
    DETECTED_COLOR = "\033[92m" # green
    STABLE_COLOR = "\033[93m" # yellow
    FALL_COLOR = "\033[94m" # blue
    LOSS_COLOR = "\033[95m" # dark purple
    DRAWING_COLOR = "\033[38;5;208m" # orange
    EXPLODE_COLOR = "\033[38;5;206m" # pink
    
    # generate special color change as time
    def SPECIAL_COLOR()->str:
        return f"\033[38;2;{abs(256 - (int(time.time() * 100) % 512))};{abs(256 - ((int(time.time() * 100) + 128) % 512))};0m"