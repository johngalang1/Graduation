# testing branch
# Import the library
from tkinter import * a

# Create an instance of tkinter frame
win = Tk()

# Define the geometry of window
win.geometry("2560x1664")

# Set the background color to white
win.config(bg="white")

#--------------------------------------------------------------------------------------------------------------------------------------

# Making Circle 

# Create a canvas object for the circle
circle_canvas = Canvas(win, width=500, height=500, bg="white")  # Set canvas background to white
circle_canvas.pack()

# Get the center of the canvas
center_x = 500 // 2
center_y = 500 // 2
radius = 200

# Draw the circle, adjusting by radius to center it with a thicker outline
circle_canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black", width=10)

#--------------------------------------------------------------------------------------------------------------------------------------

# Making Buttons 

# Create a frame for buttons below the circle
button_frame = Frame(win, bg="white")  # Set button frame background to white
button_frame.pack(pady=20)  # Add some vertical padding

# Create buttons
button1 = Button(button_frame, text="No Music")
button1.pack(side=LEFT, padx=10)  # Add horizontal padding between buttons

button2 = Button(button_frame, text="Campfire Sound")
button2.pack(side=LEFT, padx=10)

button3 = Button(button_frame, text="Waves")
button3.pack(side=LEFT, padx=10)

button4 = Button(button_frame, text="Rain")
button4.pack(side=LEFT, padx=10)

# Start the Tkinter event loop
win.mainloop()
