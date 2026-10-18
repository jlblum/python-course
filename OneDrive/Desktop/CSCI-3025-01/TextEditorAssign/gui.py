import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

"""The GuiWindow class provides the graphical window, text menu, and text entry field area."""

class GuiWindow:

    def __init__(self, root, io):
        self.root = root
        self.io = io
        self.textarea = self.create_text_component()


        self.menu = tk.Menu(self.root)      #Add Menu bar

        self.fileMenu = tk.Menu(self.menu,tearoff=0) #Add file Menu to main menu

        #Add commands to file menu
        self.fileMenu.add_command(label="New File",command=self.io.newFile)
        self.fileMenu.add_command(label="Open File",command=self.io.openFile)
        self.fileMenu.add_command(label="Save File",command=self.io.saveFile)
        self.fileMenu.add_command(label="Save File As",command=self.io.saveAsFile)
        self.fileMenu.add_command(label="Exit",command=self.io.exitProgram)

        self.aboutMenu = tk.Menu(self.menu,tearoff=0) #Add about to main menu

        self.aboutMenu.add_command(label="Program Info",command=self.io.displayAbout)
        
        self.menu.add_cascade(label="File",menu=self.fileMenu)
        self.menu.add_cascade(label="About",menu=self.aboutMenu)


        self.root.config(menu=self.menu)

    def create_text_component(self):
            """Builds and packs the scrollable text canvas."""
            text_widget = scrolledtext.ScrolledText(
                self.root, 
                wrap=tk.WORD, 
                font=("Courier New", 12), 
                undo=True
            )
            text_widget.pack(fill=tk.BOTH, expand=True)
            return text_widget