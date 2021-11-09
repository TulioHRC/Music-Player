from tkinter import *

def createScrollableFrame(mainFrame, color="#353638"):
    # Creating Canvas
    canvas = Canvas(mainFrame, bg=color)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    # Adding ScrollBar
    scroll = Scrollbar(mainFrame, orient=VERTICAL, command=canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)
    # Configuring Canvas
    canvas.configure(yscrollcommand=scroll.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    # New Frame
    newFrame = Frame(canvas)
    canvas.create_window((0,0), window=newFrame, anchor="nw")

    return newFrame
