# Import the library
from tkinter import *

# Create an instance of tkinter frame
win = Tk()

# Define the geometry of window
win.geometry("2560x1664")

# Create a canvas object for the circle
circle_canvas = Canvas(win, width=500, height=500)
circle_canvas.pack()

# Get the center of the canvas
center_x = 500 // 2
center_y = 500 // 2
radius = 200

# Draw the circle, adjusting by radius to center it with a thicker outline
circle_canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black", width=10)

win.mainloop()
