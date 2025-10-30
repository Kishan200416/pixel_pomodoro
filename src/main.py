import tkinter as tk
from PIL import Image, ImageTk # This will allow Pillow to load PNGs
import os
import time # For time.sleep()
import threading    # To create the 'worker' thread

# --- Constant ---
WINDOW_TITLE = "Pixel Pomodoro"
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 350
BG_COLOR = "#C6534B" # Red Pomodoro color
FG_COLOR = "#FFFFFF" 
FONT_NAME = "Press Start 2P" # Got it from google

# ---Timer Constants---
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

# --- Main Application Class ---
class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- The Main Window Configurations ---
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.config(bg=BG_COLOR)

        # --- Load the Tomato Image ---
        image_path = os.path.join("assets","pomodoro.png")

        try:
            # Opening the image with Pillow
            img = Image.open(image_path)

            # Resize to fit nicely as a Icon
            img = img.resize((32,32), Image.LANCZOS)

            # Must be saved to 'self' to prevent it from being garbage-collected (disappearing).
            self.tomato_image = ImageTk.PhotoImage(img)
            
            # App Icon
            self.iconphoto(True, self.tomato_image)

        except Exception as e:
            # Error Loading the Image
            print(f"Error occured Loading Image: {e}")
        
        # --- Timer Label ---
        self.timer_label = tk.Label(
            self,
            text = f"{WORK_MIN:02}:00",
            font=(FONT_NAME, 40, "bold"),
            fg = FG_COLOR,
            bg = BG_COLOR
        )
        self.timer_label.pack(pady=50)





# --- Run the App ---
if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()