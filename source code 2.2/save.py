import time
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

from helpers import addValue
__all__ = ["saveMessagestxt"] #, "saveMessageshtml"]

def saveMessagestxt(displayBox):
    text = displayBox.get(0.0, "end").split("\n")
    if text != ["", ""]:
        filename = ("Inquit-"+
                    str(time.time())+
                    ".txt")
        Tk().withdraw()
        filename = asksaveasfilename(initialdir = "/",
                                     title = "Save Messages",
                                     filetypes = [("Text File","*.txt")],
                                     confirmoverwrite=True,
                                     initialfile=filename) # show an "Open" dialog box and return the path to the selected file
        
        if filename:
            with open(filename, "w") as f:
                f.write("\n".join(text))
            
            addValue(displayBox, "\n ----- Saved to " + filename + " -----\n\n", tag="comment")

def saveMessageshtml(displayBox):
    filename = ("Inquit-"+
                decode(roomCode[6:], "whats9+10")+
                "-"+
                str(time())+
                ".html").replace(":", "-")
    Tk().withdraw()
    filename = asksaveasfilename(initialdir = "/",
                                 title = "Save messages",
                                 filetypes = [("html file","*.html")],
                                 confirmoverwrite=True,
                                 initialfile=filename) # show an "Open" dialog box and return the path to the selected file
    f = open(filename, "w")
    text = displayBox.get(3.0, END)
    f.write(text)
    f.close()
    addValue(displayBox, "\n ----- Saved to " + filename + " -----\n\n", tag="comment")
