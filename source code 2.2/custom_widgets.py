from tkinter import Label, PhotoImage, Toplevel, Button, Canvas, Tk
from tkinter.ttk import Notebook, Style
import webbrowser
import sys

class HyperlinkManager:
    def __init__(self, text):
        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, url):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-" + str(len(self.links))
        self.links[tag] = lambda :webbrowser.open_new(url)
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names("current"):
            if tag.startswith("hyper-"): #tag[:6] == "hyper-"
                self.links[tag]()
                return

class DrawWindow:
    def __init__(self, master):
        self.master = master
        self.points = set()
        self.lineWidth = 5
        self.colour = "#ff0000"
        self.createWindow()
        self.createCanvas()
        
        self.window.mainloop()

    def createWindow(self):
        self.window = Toplevel(self.master)
        self.window.title("Canvas")
        self.window.resizable(False, False)
        self.window.lift(aboveThis=self.master)
        self.window.focus_force()
    
    def createCanvas(self):
        self.canvas = Canvas(self.window, width=100, height=50, bg="#ffffff")
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        self.canvas.bind("<B1-Motion>", self.bindPaint)
        
        saveButton = Button(self.window, text="save", command=lambda: self.save)
        saveButton.pack(side="left", padx=90, fill="x", anchor="center", expand=1, pady=5)
        
        clearButton = Button(self.window, text="clear", command=lambda: self.canvas.delete("all"))
        clearButton.pack(side="left", padx=90, fill="x", anchor="center", expand=1, pady=5)
        
        closeButton = Button(self.window, text="close", command=sys.exit)
        closeButton.pack(side="left", padx=90, fill="x", anchor="center", expand=1)
    
    def bindPaint(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x-self.lineWidth//2, y-self.lineWidth//2, x+self.lineWidth//2, y+self.lineWidth//2, fill=self.colour, outline=self.colour)
        self.points.add((x, y))
    
    def save(self):
        print(self.points)

if __name__ == "__main__":
    """root = Tk()
    window = DrawWindow(root)
    #print(window.points)"""
    
    from tkinter import Tk, Frame
    def addRoom(notebook, pos="end"):
        frame = Frame(notebook, background=color)
        notebook.insert(pos, frame, text=color)
        
    root = Tk()
    
    notebook = CustomNotebook(root, addRoom, width=200, height=200)
    notebook.pack(side="top", fill="both", expand=True)

    for color in ("red", "orange", "green", "blue", "violet"):
        frame = Frame(notebook, background=color)
        notebook.add(frame, text=color)
    
    root.mainloop()
