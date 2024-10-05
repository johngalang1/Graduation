from tkinter import *
from PIL import Image, ImageTk
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#D50032"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.25  # Set for testing, adjust as needed
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
reps = 0
timer = None
is_paused = False
paused_time = 0

# ---------------------------- SOUND FUNCTIONS ------------------------------- #
def play_sound(sound_file):
    pygame.mixer.music.stop()
    if sound_file:  # Avoid loading None
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

# ---------------------------- TIMER FUNCTIONS ------------------------------- #
def reset_timer():
    global reps, is_paused, paused_time
    reps = 0
    is_paused = False
    paused_time = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark_label.config(text="")
    pause_button.config(text="Pause")
    start_button.config(state="normal")  # Re-enable start button
    canvas.itemconfig(timer_image, image=work_img)  # Reset to work image

def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=YELLOW)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=YELLOW)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)

    start_button.config(state="disabled")  # Disable start button after pressed

def pause_timer():
    global is_paused
    if is_paused:
        count_down(paused_time)
        pause_button.config(text="Pause")
        is_paused = False
    else:
        window.after_cancel(timer)
        pause_button.config(text="Resume")
        is_paused = True

def count_down(count):
    global timer, paused_time
    count_min = count // 60
    count_sec = count % 60
    paused_time = count  # Store the remaining time

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        for _ in range(reps // 2):
            marks += CHECK_MARK
        checkmark_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.geometry("2560x1664")
window.config(bg=RED)

# Load images
work_img = PhotoImage(file="download.png")  # Your work image file
break_img = PhotoImage(file="break.png")  # Your break image file

# Create a canvas for the timer display
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
timer_image = canvas.create_image(100, 112, image=work_img)  # Initial work image
timer_text = canvas.create_text(100, 130, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# Timer label and buttons
timer_label = Label(text="Timer", bg=RED, fg=GREEN, font=(FONT_NAME, 50))
timer_label.grid(row=0, column=1)

start_button = Button(text="Start", highlightbackground=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightbackground=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

pause_button = Button(text="Pause", highlightbackground=YELLOW, highlightthickness=0, command=pause_timer)
pause_button.grid(row=2, column=1)

checkmark_label = Label(fg=GREEN, bg=RED)
checkmark_label.grid(row=3, column=1)

#--------------------------------------------------------------------------------------------------------------------------------------

# Making Circle 

# Create a canvas object for the circle
circle_canvas = Canvas(window, width=500, height=500, bg="white")  # Set canvas background to white
circle_canvas.pack()

# Get the center of the canvas
center_x = 500 // 2
center_y = 500 // 2
radius = 200

# Draw the circle, adjusting by radius to center it with a thicker outline
circle_canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black", width=10)

#--------------------------------------------------------------------------------------------------------------------------------------

# Making Sound Buttons 

# Create a frame for sound buttons below the circle
button_frame = Frame(window, bg="white")  # Set button frame background to white
button_frame.pack(pady=20)  # Add some vertical padding

# Load and resize images
def load_image(image_path, size):
    img = Image.open(image_path)  # Open the image file
    img = img.resize(size, Image.LANCZOS)  # Resize the image using LANCZOS
    return ImageTk.PhotoImage(img)  # Convert to PhotoImage
        
# Define button size (100x100 pixels)
button_size = (100, 100)

# Load resized images
no_music_img = load_image("images/no_music.png", button_size)
campfire_img = load_image("images/campfire.png", button_size)
waves_img = load_image("images/waves.png", button_size)
rain_img = load_image("images/rain.png", button_size)

# Create buttons with resized images
button1 = Button(button_frame, image=no_music_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound(None))
button1.pack(side=LEFT, padx=10)

button2 = Button(button_frame, image=campfire_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/campfire_sound.mp3"))
button2.pack(side=LEFT, padx=10)

button3 = Button(button_frame, image=waves_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/waves_sound.mp3"))
button3.pack(side=LEFT, padx=10)

button4 = Button(button_frame, image=rain_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/rain_sound.mp3"))
button4.pack(side=LEFT, padx=10)

# Start the Tkinter event loop
window.mainloop()
