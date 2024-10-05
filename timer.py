from tkinter import *
from PIL import Image, ImageTk
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#D50032"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
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

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)

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

# ---------------------------- SOUND SETUP ---------------------------- #
pygame.mixer.init()

def play_sound(sound_file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50))
timer_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="images/download.jpg")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

start_button = Button(text="Start", highlightbackground=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightbackground=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

pause_button = Button(text="Pause", highlightbackground=YELLOW, highlightthickness=0, command=pause_timer)
pause_button.grid(row=2, column=1)

checkmark_label = Label(fg=GREEN, bg=YELLOW)
checkmark_label.grid(row=3, column=1)

window.mainloop()
