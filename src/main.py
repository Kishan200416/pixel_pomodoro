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
BUTTON_COLOR = "#DAA520"
FONT_NAME = "Press Start 2P" # Got it from google

# ---Timer Constants---
WORK_MIN = 1
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

        # --- Timer Variables ---
        self.current_seconds = WORK_MIN * 60
        self.timer_running = False
        self.timer_thread = None

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

        # --- Button Frame ---
        self.button_frame = tk.Frame(self, bg=BG_COLOR)
        self.button_frame.pack(pady=20)

        # ---Start Button ---
        self.start_button = tk.Button(
            self.button_frame,
            text='Start',
            font=(FONT_NAME, 14, "bold"),
            bg= BUTTON_COLOR,
            fg=FG_COLOR,
            command= self.start_timer_thread
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        # --- Reset Button ---

        self.reset_button = tk.Button(
            self.button_frame,
            text = 'Reset',
            font = (FONT_NAME, 14, "bold"),
            bg = BUTTON_COLOR,
            fg = FG_COLOR,
            command= self.reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def start_timer_thread(self):
        # Dont Start Timer if One Already On
        if self.timer_running:
            return
        
        self.timer_running = True

        self.timer_thread = threading.Thread(
            target = self.countdown_logic, #Hiring a worker to run the count_down logic
            daemon=True
        )
        self.timer_thread.start()
    
    def countdown_logic(self):

        while self.current_seconds > 0 and self.timer_running:
            #Calculate the minutes and seconds
            mins, secs = divmod(self.current_seconds, 60)

            #Format Time String
            time_string = f"{mins:02}:{secs:02}"

            # Update The Label's Text
            self.timer_label.config(text=time_string)

            # Wait for a Second
            time.sleep(1)

            # Decrementing the time
            self.current_seconds -= 1

        self.timer_label.config(text="00:00")

        # --- After the loop ---
        if self.timer_running:
            self.timer_running = False
            print("Timer Finished!") # Break Logic

    def reset_timer(self):

        #Fire the worker thread by setting False
        self.timer_running = False

        #Reset to the Beginning
        self.current_seconds = WORK_MIN * 60

        # Manually Update the Label to show reset time
        self.timer_label.config(text=f"{WORK_MIN:02}:00")
    


    





# --- Run the App ---
if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()