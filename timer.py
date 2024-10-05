from tkinter import *
from PIL import Image, ImageTk
import pygame

pygame.mixer.init()

def play_sound(sound_file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

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
reps = 0
timer = None
is_paused = False
paused_time = 0

# ---------------------------- TIMER RESET ------------------------------- # 
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

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=YELLOW)
        canvas.itemconfig(timer_image, image=break_img)  # Set break image
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=YELLOW)
        canvas.itemconfig(timer_image, image=break_img)  # Set break image
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)
        canvas.itemconfig(timer_image, image=work_img)  # Set work image

    start_button.config(state="disabled")  # Disable start button after pressed

# ---------------------------- PAUSE/RESUME MECHANISM ------------------------------- #
def pause_timer():
    global is_paused
    if is_paused:
        # If already paused, resume the timer
        count_down(paused_time)
        pause_button.config(text="Pause")
        is_paused = False
    else:
        # If not paused, stop the timer
        window.after_cancel(timer)
        pause_button.config(text="Resume")
        is_paused = True

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
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
            marks += f"{CHECK_MARK}"
        checkmark_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("GRADUATION - Pomodoro Timer")
window.geometry("2560x1664") 
window.config(padx=100, pady=50, bg=RED)

# Load images
work_img = PhotoImage(file="images/download.png")  # Your work image file
break_img = PhotoImage(file="images/break.png")  # Your break image file

timer_label = Label(text="Timer", bg=RED, fg=GREEN, font=(FONT_NAME, 50))
timer_label.grid(row=0, column=1, columnspan=2)

canvas = Canvas(width=200, height=224, bg=RED, highlightthickness=0)
timer_image = canvas.create_image(100, 112, image=work_img)  # Initial work image
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1, columnspan=2)

start_button = Button(text="Start", highlightbackground=RED, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightbackground=RED, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=3)

pause_button = Button(text="Pause", highlightbackground=RED, highlightthickness=0, command=pause_timer)
pause_button.grid(row=2, column=1, columnspan=2)

# Load and resize images
def load_image(image_path, size):
    img = Image.open(image_path)  # Open the image file
    img = img.resize(size, Image.Resampling.LANCZOS)  # Resize the image using LANCZOS (replacement for ANTIALIAS)
    return ImageTk.PhotoImage(img)  # Convert to PhotoImage
        
# Define button size (100x100 pixels)
button_size = (100, 100)
# New buttons that fit in the same width as the above three
no_music_img = load_image("images/no_music.png", button_size)
campfire_img = load_image("images/campfire.png", button_size)
waves_img = load_image("images/waves.png", button_size)
rain_img = load_image("images/rain.png", button_size)

no_music_button = Button(image=no_music_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound(None))
campfire_button = Button(image=campfire_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/campfire_sound.mp3"))
waves_button = Button(image=waves_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/waves_sound.mp3"))
rain_button = Button(image=rain_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/rain_sound.mp3"))

# Placing the new buttons in row 3, and adjusting the column span
no_music_button.grid(row=3, column=0, pady=(10, 0))
campfire_button.grid(row=3, column=1, pady=(10, 0))
waves_button.grid(row=3, column=2, pady=(10, 0))
rain_button.grid(row=3, column=3, pady=(10, 0))

# Configure column spans and weights to distribute the new buttons evenly
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)

#checkmark_label = Label(fg=GREEN, bg=RED)
#checkmark_label.grid(row=3, column=1)

window.mainloop()
