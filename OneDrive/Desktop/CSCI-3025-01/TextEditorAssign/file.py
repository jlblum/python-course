import os

"""The File class provides the disk access functions."""

class File:

    def __init__(self):
        self.currentPath = None

    def readFile(self,filePath):
        """Open a file"""
        try:
            with open(filePath, "r", encoding = "utf-8") as file: 
                content = file.read()
                self.currentPath = filePath
                return content
        
        except FileNotFoundError:
            print(f"Log: System could not find file -> {os.error}")
            return None
        except PermissionError:
            print("Could not read file, permission denied!")
            return None

    def createFile(self,text):
        """Create new file, or overwrite a file"""
        with open(self.currentPath,"w",encoding = "utf-8") as file:
            file.write(text)

    def getFilename(self):
        """Extracts the base filename from the path saved in self."""
        return os.path.basename(self.currentPath) if self.currentPath else "Untitled"
    
          