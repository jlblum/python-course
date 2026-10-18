import tkinter as tk
from gui import GuiWindow
from file import File
from editorIO import Io
import sys
import os

"""This is the main module of the program. It serves mostly as a place to instantiate the 
individual classes required to make the program function. Also provides the main loop."""

def main():

    root=tk.Tk()
    root.geometry("640x480")

    file = File() # instance of File

    editorio = Io(root, file, None) #instance of the editor I/O 
    
    gui = GuiWindow(root, editorio) #instance of the GUI
    
    editorio.textarea = gui.textarea # passing the text area into the GUI self 

    titleAtStart = file.getFilename()
    editorio.setName(titleAtStart)

    
    root.mainloop()

if __name__ == "__main__":
    main()

