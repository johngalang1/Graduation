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
WHITE = "#ffffff"
GOLD = "#d7a858"
FONT_NAME = "MS Sans Serif"
WORK_MIN = 0.25  # Set for testing, adjust as needed
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"
reps = 0
timer = None
is_paused = False
paused_time = 0
task_entries = []
task_vars = []

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, is_paused, paused_time
    reps = 0
    is_paused = False
    paused_time = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"00:00")
    timer_label.config(text="Timer", fg=GREEN)
    pause_button.config(text="Pause")
    start_button.config(state="normal")  # Re-enable start button
    canvas.itemconfig(timer_image, image=work_img)
    
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
        play_sound("music/kanye_good_morning.mp3")

    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=YELLOW)
        canvas.itemconfig(timer_image, image=break_img)  # Set break image
        play_sound("music/kanye_good_morning.mp3")

    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)
        canvas.itemconfig(timer_image, image=work_img)  # Set work image
        play_sound("music/how-sway-1.mp3")

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
        #checkmark_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MY BEAUTIFUL DARK TWISTED POMODORO")
window.geometry("2560x1664") 
window.config(padx=100, pady=50, bg=RED)

def load_and_resize_image(file_path, size):
    image = Image.open(file_path)
    resized_image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

work_img = load_and_resize_image("images/download.png", (385, 385))
break_img = load_and_resize_image("images/break.png", (385, 385))

timer_label = Label(text="Timer", bg=RED, fg=GREEN, justify="left", font=(FONT_NAME, 50))
timer_label.grid(row=0, column=1, columnspan=2)

canvas = Canvas(width=400, height=400, bg=GOLD, highlightthickness=0)
timer_image = canvas.create_image(200, 200, image=work_img)
timer_text = canvas.create_text(200, 200, text="00:00", fill=WHITE, font=(FONT_NAME, 60, "bold"))
canvas.grid(row=1, column=1, columnspan=2)

start_button = Button(text="Start", highlightbackground=RED, highlightthickness=10, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightbackground=RED, highlightthickness=10, command=reset_timer)
reset_button.grid(row=2, column=3)

pause_button = Button(text="Pause", highlightbackground=RED, highlightthickness=10, command=pause_timer)
pause_button.grid(row=2, column=1, columnspan=2)

def load_image(image_path, size):
    img = Image.open(image_path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)
        
button_size = (100, 100)
no_music_img = load_image("images/no_music.png", button_size)
campfire_img = load_image("images/campfire.png", button_size)
waves_img = load_image("images/waves.png", button_size)
rain_img = load_image("images/rain.png", button_size)

no_music_button = Button(image=no_music_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound(None))
campfire_button = Button(image=campfire_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/campfire_sound.mp3"))
waves_button = Button(image=waves_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/waves_sound.mp3"))
rain_button = Button(image=rain_img, width=100, height=100, highlightbackground="#ffffff", highlightthickness=0, command=lambda: play_sound("music/rain_sound.mp3"))
task_label = Label(text="Tasks:", bg=RED, fg=WHITE, justify="left", font=(FONT_NAME, 25))
task_label.grid(row=4, column=0)

no_music_button.grid(row=3, column=0, pady=(20, 0))
campfire_button.grid(row=3, column=1, pady=(20, 0))
waves_button.grid(row=3, column=2, pady=(20, 0))
rain_button.grid(row=3, column=3, pady=(20, 0))

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)

for i in range(3):
    var = BooleanVar()
    task_vars.append(var)

    task_entry = Entry(window, width=15, justify="left", font=(FONT_NAME, 12), fg=GREEN)
    task_entry.grid(row=4 + i, column=1, padx=5, pady=(10, 0))
    task_entry.insert(0, f"Task {i+1}")
    task_entries.append(task_entry)

    def create_task_check(entry, var):
        def check_task():
            if var.get():
                entry.config(fg=RED, font=(FONT_NAME, 12, "italic"))
            else:
                entry.config(fg=GREEN, font=(FONT_NAME, 12, "normal"))
        return check_task

    checkbox = Checkbutton(window, variable=var, background=RED,command=create_task_check(task_entry, var))
    checkbox.grid(row=4 + i, column=2)

window.mainloop()
