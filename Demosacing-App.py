# Import the library tkinter
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from imageio import imread, imwrite
import numpy as np
import ntpath
from scipy import ndimage
# global variables
selectedFile = "empty"
option = "RGGB"
# function to convert RGB image to RAW


def convert_rgb():
    global selectedFile
    global option
    img = imread(selectedFile)
    raw = np.zeros((img.shape[0], img.shape[1]))
    if option == "RGGB":
        print(option+" image converted to RAW")
        raw[::2, ::2] = img[::2, ::2, 0]
        raw[1::2, ::2] = img[1::2, ::2, 1]
        raw[::2, 1::2] = img[::2, 1::2, 1]
        raw[1::2, 1::2] = img[1::2, 1::2, 2]
    elif option == "BGGR":
        print(option+" image converted to RAW")
        raw[1::2, 1::2] = img[1::2, 1::2, 0]
        raw[1::2, ::2] = img[1::2, ::2, 1]
        raw[::2, 1::2] = img[::2, 1::2, 1]
        raw[::2, ::2] = img[::2, ::2, 2]
    elif option == "GRBG":
        print(option+" image converted to RAW")
        raw[::2, 1::2] = img[::2, 1::2, 0]
        raw[::2, ::2] = img[::2, ::2, 1]
        raw[1::2, 1::2] = img[1::2, 1::2, 1]
        raw[1::2, ::2] = img[1::2, ::2, 2]
    elif option == "GBRG":
        print(option+" image converted to RAW")
        raw[1::2, ::2] = img[1::2, ::2, 0]
        raw[::2, ::2] = img[::2, ::2, 1]
        raw[1::2, 1::2] = img[1::2, 1::2, 1]
        raw[::2, 1::2] = img[::2, 1::2, 2]
    saveImg = ntpath.basename(selectedFile)
    imwrite("RAW("+option+")_"+saveImg, np.uint8(raw))

# function to convert RAW image to RGB


def convert_raw():
    global selectedFile
    global option
    raw = np.float32(imread(selectedFile))
    green = np.zeros(raw.shape)
    green[1::2, ::2] = raw[1::2, ::2]
    green[::2, 1::2] = raw[::2, 1::2]
    missing_green = ndimage.correlate(raw, np.array([[0, 1, 0],
                                                     [1, 0, 1],
                                                     [0, 1, 0]])/4)
    green[::2, ::2] = missing_green[::2, ::2]
    green[1::2, 1::2] = missing_green[1::2, 1::2]
    red = np.zeros(raw.shape)
    red[::2, ::2] = raw[::2, ::2]
    missing_red = ndimage.correlate(raw, np.array([[1, 0, 1],
                                                   [0, 0, 0],
                                                   [1, 0, 1]])/4)
    red[1::2, 1::2] = missing_red[1::2, 1::2]
    blue = np.zeros(raw.shape)
    blue[1::2, 1::2] = raw[1::2, 1::2]
    missing_blue = ndimage.correlate(raw, np.array([[1, 0, 1],
                                                    [0, 0, 0],
                                                    [1, 0, 1]])/4)
    blue[::2, ::2] = missing_blue[::2, ::2]
    missing_red = ndimage.correlate(raw, np.array([[0, 1, 0],
                                                   [1, 0, 1],
                                                   [0, 1, 0]])/4)
    red[1::2, ::2] = missing_red[1::2, ::2]
    red[::2, 1::2] = missing_red[::2, 1::2]
    missing_blue = ndimage.correlate(raw, np.array([[0, 1, 0],
                                                    [1, 0, 1],
                                                    [0, 1, 0]])/4)
    blue[1::2, ::2] = missing_blue[1::2, ::2]
    blue[::2, 1::2] = missing_blue[::2, 1::2]
    full_rgb = np.zeros((raw.shape[0], raw.shape[1], 3))
    full_rgb[:, :, 0] = red
    full_rgb[:, :, 1] = green
    full_rgb[:, :, 2] = blue
    saveImg = selectedFile.replace('RAW', 'RGB')
    imwrite(saveImg, np.uint8(np.clip(full_rgb, 0, 255)))
    print("image converted into rgb")


# Create a GUI app
root = tk.Tk()
# Adjust size
root.geometry("960x640")
# Give title to your GUI app
root.title("Demosaic App")
root.config(bg='white')
# Add image file
bg = PhotoImage(file="demosaic.png")
img = PhotoImage(file="demosaic.png")
label = Label(
    root,
    image=img
)
label.place(x=0, y=0)
# Create Canvas
canvas1 = Canvas(root, width=960,
                 height=480)

canvas1.pack(fill="both", expand=True)
# Display image
canvas1.create_image(0, 0, image=bg,
                     anchor="nw")
# Heading of project
canvas1.create_text(
    480, 80, text="Demosaicing", font=("Arial", 36), fill="yellow")
canvas1.create_text(
    480, 120, text="Color Reconstruction", font=("Arial", 18), fill="yellow")
label_file_explorer = Label(root,
                            text="Selected Image Path",
                            width=60, height=2,
                            fg="blue")

# function to open windows explorer


def open():
    global selectedFile
    f_types = [('PNG Files', '.png'), ('Jpg Files', '.jpg')]
    selectedFile = filedialog.askopenfilename(
        initialdir='/', title="Select A File", filetypes=f_types)
    label_file_explorer.configure(text="File Opened: "+selectedFile)


# Creating button to select image
button = Button(
    root,
    text='Select Your Image Here',
    relief=RAISED,
    font=('Arial', 14),
    command=lambda: open()
)

# positioning the button
button.place(x=50, y=150)
# positioning the path descriptor
label_file_explorer.place(x=50, y=220)


# Creating button to convert into raw
button1 = Button(
    root,
    text='Convert Into RAW Image ',
    relief=RAISED,
    font=('Arial', 14),
    command=lambda: convert_rgb()
)
# positioning the button
button1.place(x=50, y=360)

# Creating button to convert into rgb
button2 = Button(
    root,
    text='Convert Into RGB Image ',
    relief=RAISED,
    font=('Arial', 14),
    command=lambda: convert_raw()
)
# positioning the button
button2.place(x=50, y=430)

# defining a label
Label(root, text="Select Your Bayer Pattern", bg="black", fg="white",
      borderwidth=3, relief="flat", padx=5, pady=10).place(x=50, y=290)

# getting option from dropdown menu


def get_option(choice):
    global option
    choice = clicked.get()
    option = choice
    print(option)


# Dropdown menu options
options = [
    "RGGB",
    "BGGR",
    "GRBG",
    "GBRG",
]

# datatype of menu text
clicked = StringVar()
# initial menu text
clicked.set(options[0])
# Create Dropdown menu
drop = OptionMenu(root, clicked, *options, command=get_option)
drop.place(x=220, y=295)
# Make the loop for displaying app
root.mainloop()
