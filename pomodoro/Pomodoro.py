from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"
reps = 0
timer = None
is_paused = False  # To track if the timer is paused
remaining_time = 0  # To store the remaining time when paused


task_labels = []
task_vars = []

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, is_paused, remaining_time
    reps = 0
    is_paused = False
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark_label.config(text="")
    reset_tasks()

def reset_tasks():
    for var in task_vars:
        var.set(False)  # Uncheck all checkboxes
    for entry in task_labels:
        entry.delete(0, END)  # Clear all entries

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, remaining_time, is_paused
    if not is_paused:
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

    if not is_paused:  # Start countdown only if not paused
        count_down(remaining_time)

    count_down(remaining_time)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global timer, is_paused, remaining_time

    if is_paused:
        return  # Stop the countdown if paused
    
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        for _ in range(reps//2):
            marks += f"{CHECK_MARK}"
        checkmark_label.config(text=marks)


def pause_timer():
    global is_paused
    if is_paused:
        is_paused = False
        start_timer()  # Resume the timer
        pause_button.config(text="Pause")  # Change button text back to "Pause"
    else:
        is_paused = True  # Pause the timer
        window.after_cancel(timer)  # Stop the countdown
        pause_button.config(text="Resume")  # Change button text to "Resume"



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", bg=YELLOW, fg= GREEN, font=(FONT_NAME, 50))
timer_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file= "tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

start_button = Button(text="Start", highlightbackground=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

pause_button = Button(text="Pause", highlightbackground=YELLOW, highlightthickness=0, command=pause_timer)
pause_button.grid(row=2, column=1)  # Add the pause button in the middle

reset_button = Button(text="Reset", highlightbackground=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)


checkmark_label = Label(fg=GREEN, bg=YELLOW)
checkmark_label.grid(row=3, column=1)


# Task input grid
for i in range(3):
    for j in range(3):
        var = BooleanVar()  # Variable to hold the checkbox state
        task_vars.append(var)

        task_label = Label(window, text=f"Task {i*3+j+1}", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 12))
        task_label.grid(row=4 + i, column=j, padx=5, pady=5)
        task_labels.append(task_label)

        # Checkbox to check off tasks
        def create_task_check(label, var):
            def check_task():
                if var.get():
                    label.config(fg=RED, text=f"~~ {label.cget('text')} ~~")  # Strike-through effect
                else:
                    label.config(fg=GREEN, text=label.cget('text').replace("~~ ", "").replace(" ~~", ""))  # Restore
            return check_task
        
        checkbox = Checkbutton(window, variable=var, command=create_task_check(task_label, var))
        checkbox.grid(row=4 + i, column=j + 3)

window.mainloop()