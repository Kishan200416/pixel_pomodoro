import tkinter as tk
from PIL import Image, ImageTk # This will allow Pillow to load PNGs
import os
import time # For time.sleep()
import threading    # To create the 'worker' thread

# -- Constant --
WINDOW_TITLE = "Pixel Pomodoro"
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 350
BG_COLOR = "#2b2b2b" # A nice dark grey
FG_COLOR = "#f0f0f0" 
FONT_NAME = "Press Start 2P" # Got it from google

# --Timer Constants--
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

# -- Main Application Class --
class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()