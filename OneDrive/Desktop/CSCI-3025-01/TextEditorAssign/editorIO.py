from tkinter import filedialog, messagebox, END
import file
import os

"""The IO class works to connect the options provided in the GUI menu, to the appropriate File
class functions. Also provides exit and about functions. """

class Io:


    def __init__(self, root, file, textarea):
        self.root = root
        self.textarea = textarea
        self.currentFile = file

    def setName(self,name):
        """Sets the filename to be displayed in the editor"""
        self.root.title(f"CSCI 3025 Text Editor - {name}")

    def newFile(self):
            if not self.textarea:
                  return
            self.textarea.delete("1.0", END)
            self.currentFile.currentPath = None
            self.setName("Untitled")

    def openFile(self):     
      
        if not self.textarea:
                return
          
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],defaultextension=".*")
        if file_path:
            try:
                content = self.currentFile.readFile(file_path)
                self.textarea.delete("1.0", END)
                print(content)
                self.textarea.insert("1.0", content)
                self.setName(self.currentFile.getFilename())

            except Exception as e:
                messagebox.showerror("Error", f"opening file: {e}")    
                      
    def saveFile(self):
        if not self.textarea:
              return

        if self.currentFile.currentPath:
            try:
                content = self.textarea.get("1.0",END)
                self.currentFile.createFile(content)
                self.setName(self.currentFile.getFilename())
            except Exception as e:
                 messagebox.showerror("Error", f"saving file: {e}")
        else:
             self.saveAsFile()        # if the file has not been saved before, open file dialog to name it.
        

    def saveAsFile(self):
        if not self.textarea:
            return
        file_path = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],defaultextension=".*")
        if file_path:
            try:
                  content = self.textarea.get("1.0",END)
                  self.currentFile.currentPath = file_path 
                  self.currentFile.createFile(content)
                  self.setName(self.currentFile.getFilename())
            except Exception as e:
                 messagebox.showerror("Error", f"saving file : {e}")
                 
    def exitProgram(self):
            self.root.quit()

    def displayAbout(self):
            messagebox.showinfo(title="About this program", message="CSC3025 Module 5 programming assignment\nModular code\nJesse L Blum\n2026")