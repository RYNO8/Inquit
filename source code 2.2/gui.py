from tkinter import Frame, Menu, Tk, PhotoImage, Button
from tkinter.ttk import Style, Notebook
import os

from helpers import colourConversion, Settings
import loading
from tab import Tab
from get_room import GetRoom
from options_bar import showAboutMenu, showHelpMenu, customise
from text_handle import sendMsg
from save import saveMessagestxt

class Inquit:
    def __init__(self, master, net, settings, text="", state="", roomLimit=15, wW=1000, wH=600):
        """\
master = Tk()
state = "fullscreen" "maximised" ""
"""
        self.settings = settings
        self.net = net
        self.text = text
        self.master = master
        self.roomLimit = roomLimit
        self.tabs = []
        if state == "fullscreen":
            self.master.attributes("-fullscreen", True)
        elif state == "maximised":
            self.master.state("zoomed")
        self.master.title("Inquit: New Room")
        self.master.geometry(str(wW) + "x" + str(wH) + "+100+100")
        self.master.after(1, lambda: self.master.focus_force())
        
        self.createMenu()
        self.createNewButton()
        self.createNotebook()
        
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.bind("<Control-w>", self.onClose)
        self.master.bind("<Control-t>", self.onOpen)
        self.master.bind("<ButtonRelease-1>", self.onClose)
        self.master.bind("<Return>", self.onEnter)
        self.master.bind("<FocusIn>", self.gainFocus)
        self.master.bind("<FocusOut>", self.loseFocus)
        
        self.prevIndex = 0
        self.addRoom(text=text)
    
    def numRooms(self):
        return self.notebook.index("end") #nunTabs
    
    def createNewButton(self):
        self.newTabButton = Button(self.master, text="New Tab", command=self.onOpen)
        self.newTabButton.pack(side="top", anchor="ne")
        
    def onOpen(self, *args):
        self.prevIndex = self.notebook.index(self.notebook.select())
        if self.numRooms() < self.roomLimit:
                self.addRoom()
    
    def onClose(self, event=None):
        """Called when the user wants to close a tab"""
        toCluse = False
        if event.keysym == "w":
            element = self.notebook.select()
            index = self.notebook.index(element)
            toClose = True
            
        else:
            element = self.notebook.identify(event.x, event.y)
            toClose = "close" in element
            try:
                index = self.notebook.index("@%d,%d" % (event.x, event.y))
            except:
                return
        
        if toClose:
            try: #TODO: test this
                path = os.environ.get("APPDATA") + "\\Microsoft\\Windows\\Start Menu\\Programs\\" + self.tabs[index][1].roomName + ".lnk"
                os.remove(path) #this may be dangerous
                print("removed link")
            except (FileNotFoundError, AttributeError, OSError):
                pass
            
            self.notebook.forget(index)
            self.notebook.event_generate("<<NotebookTabClosed>>")
            
            if self.numRooms() == 0:
                self.addRoom()
            else:
                self.notebook.select(self.prevIndex)
    
    def addRoom(self, pos="end", text=None):
        mainframe = Frame(self.notebook, borderwidth=0, highlightthickness=0)
        self.notebook.insert(pos, mainframe, text="New Room")
        self.notebook.select(mainframe)
        tabIndex = self.notebook.index("current")
        #self.prevIndex = tabIndex
        
        #SECTION 1 - get user input (get roomName)
        #print(self.settings.data)
        mainframe.after(1, lambda :self.saveSettings(self.settings, initTab=tabIndex))
        gui = GetRoom(mainframe, self.net, self.settings.prevRoom, text=text)
        self.tabs.insert(tabIndex, (mainframe, gui))
        gui.mainloop()
        
        # exit gracefully on userexit
        try:
            gui.UIframe.pack_forget()
        except:
            return
        self.settings.prevRoom = roomName = gui.roomName
        currUsers = gui.currUsers
        
        #SECTION 2 - display room
        self.notebook.tab("current", text=roomName)
        tab = Tab(mainframe, roomName, self.settings.displayName, self.net, currUsers)
        del self.tabs[tabIndex]
        self.tabs.insert(tabIndex, (mainframe, tab))
        self.saveSettings(self.settings, initTab=tabIndex)
        tab.mainloop()
            
    def createNotebook(self):
        style = Style()
        self.images = (PhotoImage("img_close", data="""R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs="""),
                       PhotoImage("img_closeactive", data="""R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs="""),
                       PhotoImage("img_closepressed", data="""R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs="""))
        style.element_create("close", "image", "img_close", ("active", "pressed", "!disabled", "img_closepressed"), ("active", "!disabled", "img_closeactive"), border=8, sticky="")
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [("CustomNotebook.tab", {"sticky": "nswe", "children": [("CustomNotebook.padding", {"side": "top", "sticky": "nswe", "children": [("CustomNotebook.focus", {"side": "top", "sticky": "nswe","children": [("CustomNotebook.label", {"side": "left", "sticky": "", }), ("CustomNotebook.close", {"side": "left", "sticky": ""}),]})]})]})])
        
        self.notebook = Notebook(self.master, width=10000, height=10000, style="CustomNotebook")
        self.notebook.enable_traversal()
        self.notebook.pack()
        
    def createMenu(self):
        self.menubar = Menu(self.master)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Save To Text", command=lambda:saveMessagestxt(self.tabs[self.notebook.index("current")][1].displayBox))
        #filemenu.add_command(label="Save To Html", command=saveMessageshtml(self.displayBox)
        filemenu.add_command(label="Settings", command=lambda:customise(self.master, self.settings, self.saveSettings))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=lambda: self.master.destroy())
        self.menubar.add_cascade(label="Home", menu=filemenu)
        
        self.menubar.add_command(label="About", command=lambda: showAboutMenu(self.master))
        self.menubar.add_command(label="Help", command=lambda: showHelpMenu(self.master))
        self.master.config(menu=self.menubar)
        
    def saveSettings(self, settings, initTab=None):
        self.settings = Settings(settings) #WARNING: override
        self.newTabButton.configure(font=(self.settings.font, self.settings.fontsize))
        self.master.configure(bg=colourConversion(self.settings.theme)["bg"])
        
        flag = False if initTab == None else True
        #print(flag, initTab)
        
        for i, (mainframe, tab) in enumerate(self.tabs):
            if initTab == i or initTab == None:
                mainframe.configure(bg=colourConversion(self.settings.theme)["bg"])
                #type(tab) == GetRoom or type(tab) == Tab
                tab.saveSettings(self.settings, init=flag)
            
    def onEnter(self, press):
        mainframe, currTab = self.tabs[self.notebook.index("current")]
        if type(currTab) == GetRoom:
            currTab.processRoomName()
        else:
            sendMsg(self.net, currTab.inputBox, currTab.roomName)
            
    def gainFocus(self, event):
        self.focus = True
        
    def loseFocus(self, event):
        self.focus = False

if __name__ == "__main__":
    from net import Net
    from copy import deepcopy
    from helpers import loadPreferences
    """style = Style()
    currTheme = style.theme_use()
    
    print(style.layout("TButton"))
    style.map("TButton",
               background=[("disabled","#d9d9d9"), ("active","#ececec")],
               foreground=[("disabled","#a3a3a3")],
               relief=[("pressed", "!disabled", "sunken")])"""
    s = loadPreferences()
    
    net = Net()
    net.setToken(s.token)
    
    root = Tk()
    inquit = Inquit(root, net, s, state="")
    root.mainloop()
    
    print(inquit.settings)

