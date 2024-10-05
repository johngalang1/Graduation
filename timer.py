from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#D50032"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.25  # Set for testing, adjust as needed
SHORT_BREAK_MIN = 5
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
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=RED)

# Load images
work_img = PhotoImage(file="download.png")  # Your work image file
break_img = PhotoImage(file="break.png")  # Your break image file

timer_label = Label(text="Timer", bg=RED, fg=GREEN, font=(FONT_NAME, 50))
timer_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=RED, highlightthickness=0)
timer_image = canvas.create_image(100, 112, image=work_img)  # Initial work image
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

start_button = Button(text="Start", highlightbackground=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightbackground=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

pause_button = Button(text="Pause", highlightbackground=YELLOW, highlightthickness=0, command=pause_timer)
pause_button.grid(row=2, column=1)

checkmark_label = Label(fg=GREEN, bg=RED)
checkmark_label.grid(row=3, column=1)

# Task input section (3 tasks)
for i in range(3):
    var = BooleanVar()  # Variable to hold the checkbox state
    task_vars.append(var)

    # Entry field for writing the task
    task_entry = Entry(window, width=20, font=(FONT_NAME, 12))
    task_entry.grid(row=4 + i, column=0, padx=5, pady=5)
    task_entries.append(task_entry)

    # Checkbox to check off tasks
    def create_task_check(entry, var):
        def check_task():
            if var.get():
                entry.config(fg=RED, font=(FONT_NAME, 12, "italic"))  # Strike-through effect
            else:
                entry.config(fg=GREEN, font=(FONT_NAME, 12, "normal"))  # Restore
        return check_task

    checkbox = Checkbutton(window, variable=var, command=create_task_check(task_entry, var))
    checkbox.grid(row=4 + i, column=1)

window.mainloop()
