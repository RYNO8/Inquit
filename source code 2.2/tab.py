from tkinter import PhotoImage, Label, Entry, Button, Frame
from tkinter.scrolledtext import ScrolledText
from random import choice
import threading

from helpers import colourConversion, addValue, LONG_ICON
from text_handle import receive, sendMsg
from user_list import UserList

__all__ = ["Tab"]

class Tab:
    def __init__(self, master, roomName, displayName, net, currUsers):
        """holds the display of messages from/to room. loads settings when called by Notepad and provides with settings (does not store settings internally)"""
        
        self.frame = master
        self.roomName = roomName
        self.displayName = displayName
        self.net = net
        self.currUsers = currUsers
        
        self.createLogo() # before DisplayBox
        self.createList()
        self.createDisplayBox()
        self.createInputBox()
        self.createEnterButton() #after InputBox
        #self.createImageButton()
        
        self.label.pack(side="top", anchor="w")
        self.displayBox.pack(side="top", padx=3, pady=3, fill="both", expand=True, relief=None)
        self.inputBox.pack(after=self.displayBox, side="left", padx=3, pady=3, fill="both", expand=True)
        self.enterButton.pack(side="right", padx=3, pady=3)
        #self.imageButton.pack(side=RIGHT, padx=3, pady=3)
        
        #img.pack(side=RIGHT)
        #addValue(self.displayBox, img)
        
    def createLogo(self):
        photo = PhotoImage(file=LONG_ICON)
        self.label = Label(self.frame, image=photo)
        self.label.image = photo # keep a reference!
        
    def createList(self):
        self.internalFrame = Frame(self.frame, width=100)
        self.internalFrame.pack(side="right", fill="y")
        self.list = UserList(self.internalFrame, self.roomName, self.net, self.currUsers, width=20)
        
    def createDisplayBox(self):
        self.displayBox = ScrolledText(self.frame, wrap="none", height=0, state="disabled", takefocus=True)
        
        #TODO: add more config
        self.displayBox.tag_configure("selfmsg", justify="right")
        self.displayBox.tag_configure("othermsg", justify="left")
        self.displayBox.tag_config("title", lmargin1=2)
        self.displayBox.tag_config("comment", justify="center")
    
    def createInputBox(self):
        self.inputBox = Entry(self.frame, borderwidth=2, takefocus=True)
        self.inputBox.focus_set()
    
    def createEnterButton(self):
        self.enterButton = Button(self.frame, text="Yeet Msg", height=1, width=13, command=lambda:sendMsg(self.net, self.inputBox, self.roomName))
        
    def createImageButton(self):
        self.imageButton = Button(self.frame, text="Yeet Image", height=1, width=13, command=sendImg)
        
    def saveSettings(self, settings, init=False):
        self.list.saveSettings(settings, init=init)
        if init: #tab just started up. these will only be called once
            addValue(self.displayBox, "\nWelcome, " + settings.displayName + "\n\n", tag="title")
            receive(self, settings.notify)
            
        self.frame.configure(bg=colourConversion(settings.theme)["bg"])
        self.label.configure(bg=colourConversion(settings.theme)["bg"])
        self.inputBox.configure(font=(settings.font, settings.fontsize))
        self.enterButton.configure(font=(settings.font, settings.fontsize))
        #self.imageButton.configure(font=(settings.font, settings.fontsize))
        
        self.displayBox.configure(font=(settings.font, settings.fontsize))
        self.displayBox.configure(bg=colourConversion(settings.theme)["bg"])
        self.displayBox.tag_configure("selfmsg", foreground=colourConversion(settings.theme)["own"])
        self.displayBox.tag_configure("othermsg", foreground=colourConversion(settings.theme)["other"])
        self.displayBox.tag_configure("title", foreground=colourConversion(settings.theme)["title"])
        self.displayBox.tag_config("comment", foreground=colourConversion(settings.theme)["title"])
        
        #perhaps fancy colours for the rest: inputBox, enterButton, imageButton

if __name__ == "__main__":
    from tkinter import Tk
    from tkinter.ttk import Notebook
    from helpers import Settings
    from net import Net
    
    net = Net()
    net.setToken(loadToken())
    #settings = {"font":"Consolas", "fontsize":11, "display_name":"Ryan", "theme":"light", "notify":"1",}
    def receive(*args):
        pass
        
    root = Tk()
    mainframe = Frame(root, bg="white", borderwidth=0, highlightthickness=0)
    
    tab = Tab(mainframe, "Public", "Ryan", net, True)
    root.bind("<Return>", lambda _:sendMsg(net, tab.inputBox, tab.roomName))
    mainframe.pack(expand=True, fill="both")
    
    root.after(1000, lambda :tab.saveSettings(Settings({"font":"Consolas", "fontsize":11, "displayName":"Ryan", "theme":"light", "notify":"1",}), init=True))
    root.mainloop()
    
