import tkinter as tk
from PIL import Image, ImageTk # This will allow Pillow to load PNGs
import os
import time # For time.sleep()
import threading    # To create the 'worker' thread
import pygame # for sound

# --- Constant ---
WINDOW_TITLE = "Pixel Pomodoro"
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 400
BG_COLOR = "#C6534B" # Red Pomodoro color
FG_COLOR = "#FFFFFF" 
BUTTON_COLOR = "#DAA520"
FONT_NAME = "Press Start 2P" # Got it from google

# ---Timer Constants---
WORK_MIN = 0.1
SHORT_BREAK_MIN = 0.2
LONG_BREAK_MIN = 0.5

# --- Main Application Class ---
class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- The Main Window Configurations ---
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.config(bg=BG_COLOR)

        # --- Initialize Audio ---
        pygame.mixer.init()
        sound_path = os.path.join("assets", "clavar_la_espada.mp3")
        self.notification_sound = pygame.mixer.Sound(sound_path)

        # --- Timer Variables ---
        self.current_seconds = WORK_MIN * 60
        self.timer_running = False
        self.timer_thread = None
        self.sessions_completed = 0
        self.current_state = "Work"

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
        self.timer_label.pack(pady=20)
        
        # --- Task Entry ---
        self.task_label = tk.Label(
            self,
            text="Task:",
            font=(FONT_NAME, 12, "bold"),
            fg=FG_COLOR,
            bg=BG_COLOR
        )
        self.task_label.pack() # Task: text

        self.task_entry = tk.Text(
            self,
            font=(FONT_NAME, 10),
            bg=FG_COLOR,
            fg=BG_COLOR,
            width=20,
            height=2,
            relief=tk.FLAT
        )
        self.task_entry.pack(pady=10)
        
        # --- Currentm State Label ---
        self.current_state_label = tk.Label(
            self,
            text="Time to focus!",
            font=(FONT_NAME, 12, "bold"),
            fg=FG_COLOR,
            bg=BG_COLOR
        )
        self.current_state_label.pack()

        # --- Session Counter Label ---
        self.session_counter_label = tk.Label(
            self,
            text=f"Sessions {self.sessions_completed}",
            font=(FONT_NAME, 10),
            fg=FG_COLOR,
            bg=BG_COLOR
        )
        self.session_counter_label.pack(pady=5)



        # --- Button Frame ---
        self.button_frame = tk.Frame(self, bg=BG_COLOR)
        self.button_frame.pack(pady=10)

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
        pygame.mixer.stop() # Stop the music
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

        # --- After the loop ---
        self.timer_running = False
        self.timer_label.config(text="00:00")

        #Call our new function
        self.setup_next_session()

        
    
    def setup_next_session(self):
        """Sets the app for the next session (Work,Short, or Long)"""

        self.notification_sound.play()

        # If the session finished was "Work" session
        if self.current_state == "Work":
            self.sessions_completed += 1
            # Update the counter label
            self.session_counter_label.config(text=f"Sessions: {self.sessions_completed}")
            

            # Check for Long Break (Every 4 sessions)
            if self.sessions_completed % 4 == 0:
                self.current_state = "Long Break"
                self.current_seconds = LONG_BREAK_MIN * 60
                self.current_state_label.config(text="Take a Long Break!")
            else:
                self.current_state = "Short Break"
                self.current_seconds = SHORT_BREAK_MIN * 60
                self.current_state_label.config(text="Take a Short Break!")
        
        #If the resting session is finished we go back to "Work"
        else:
            self.current_state = "Work"
            self.current_seconds = WORK_MIN * 60
            self.current_state_label.config(text="Time to focus!")
        
        #Update Timer Label for New Session
        mins, secs = divmod(self.current_seconds, 60)
        self.timer_label.config(text=f"{mins:02}:{secs:02}")

    def reset_timer(self):
        pygame.mixer.stop() # Stop the music
        """Resets the timer to a default 25-min Work session."""

        #Fire the worker thread by setting False
        self.timer_running = False

        #Reset all State Variables
        self.current_state = "Work"
        self.sessions_completed = 0
        self.current_seconds = WORK_MIN * 60

        # Manually Update the Label to show reset time
        self.timer_label.config(text=f"{WORK_MIN:02}:00")
        self.current_state_label.config(text="Time to focus!")
        self.session_counter_label.config(text=f"Sessions: {self.sessions_completed}")
    


    





# --- Run the App ---
if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()