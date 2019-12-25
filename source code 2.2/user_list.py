from tkinter import Frame, Entry, Button, Text
from helpers import addValue, colourConversion, runThread
import os
#receive = lambda *args:print("receive", args)

__all__ = ["Userlist"]

class UserList:
    def __init__(self, master, roomName, net, currUsers, width=20):
        """displays allowed users in a room. to be run in notepad tab under master (Frame obj)"""
        
        self.master = master
        self.roomName = roomName
        self.net = net
        self.currUsers = currUsers
        self.width = width
        
        self.createFrame()
        self.createInputBox()
        self.createEnterButton()
        self.createDisplayBox()
        
        self.frame.pack(side="right", expand=True, fill="both")
        self.inputBox.pack(side="left", expand=True, fill="both", padx=3, pady=3)
        self.enterButton.pack(side="right", padx=3, pady=3)
        self.displayBox.pack(side="bottom", before=self.inputBox, expand=True, fill="both")
        
    def createFrame(self):
        self.frame = Frame(self.master)
        
    def createInputBox(self):
        self.inputBox = Entry(self.frame, borderwidth=2, width=self.width)
    
    def createEnterButton(self):
        self.enterButton = Button(self.frame, text="Add User", height=1, width=13, command=lambda :runThread(self.onEnter))
    
    def createDisplayBox(self):
        self.displayBox = Text(self.frame, wrap="none", height=0, width=self.width, state="disabled", takefocus=True, relief="flat")
        for user in self.currUsers:
            addValue(self.displayBox, user + "\n")
        
    def saveSettings(self, settings, init=False):
        self.frame.configure(bg=colourConversion(settings.theme)["bg"])
        self.displayBox.configure(bg=colourConversion(settings.theme)["bg"])
        self.displayBox.tag_configure("selfmsg", foreground=colourConversion(settings.theme)["own"])
        self.displayBox.tag_configure("error", foreground="#ff4238")
        
    def onEnter(self):
        user = self.inputBox.get()
        self.inputBox.delete(0, "end")
        if user:
            response = self.net.post("invite", room_name=self.roomName, new_user=user)
            
            if not response["error"]:
                addValue(self.displayBox, user + "\n", tag="selfmsg")
            else:
                addValue(self.displayBox, " -" + response["error"] + "- \n", tag="error")
                #self.frame.destroy()
                #error.main()

if __name__ == "__main__":
    #from helpers import Settings
    from net import Net
    from tkinter import Tk
    from helpers import loadToken
    net = Net()
    net.setToken(loadToken())
    
    #settings = {"font":"Consolas", "fontsize":11, "display_name":"Ryan", "theme":"light", "notify":"1",}
        
    root = Tk()
    frame = Frame(root)
    frame.pack()
    app = UserList(frame, "Public",  net, ["Ryan", "Cyril"])
    #root.after(1000, lambda :tab.saveSettings(Settings({"font":"Consolas", "fontsize":11, "displayName":"Ryan", "theme":"light", "notify":"1",}), init=True))
    root.mainloop()
    
