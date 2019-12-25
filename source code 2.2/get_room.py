from tkinter import Button, Checkbutton, Entry, Frame, IntVar, Tk, Label, Text
from random import choice
from helpers import runTask, addValue, colourConversion
from urllib import parse
__all__ = ["GetRoom"]

ADJECTIVES = ["sad", "sad", "sad", "obese", "big", "exaggerated", "attractive", "bald", "beautiful", "clean", "dazzling", "flabby", "glamorous", "long", "forgetful", "lonely", "suicidal", "depressed", "bouncy", "tiny", "extrodinary", "sad", "happy", "holy", "tall", "short", "cold", "nerdy"]
NOUNS = ["chickens", "ducks", "cats", "dogs", "lions", "bears", "deers", "squirrels", "wolves", "whales", "monkeys", "rabbits", "planes", "cows", "aeroplanes", "squares", "mothers", "brothers", "slaves", "letters", "lovers", "lemon_grenades", "triangles", "pigeons", "books", "operating_systems", "teachers", "submarines"]
ADVERBS = ["extremely", "very", "overly", "ridiculously", "", "", "", ""] #options for no adverbs


class GetRoom:
    def __init__(self, master, net, roomName, text=""):
        """\
master is type frame
user input self.atSchool and self.roomName
exit without destroying master"""
        self.master = master
        self.net = net
        self.roomName = roomName
        self.text = text
        self.displayBox = Text(self.master) #for saveMessagestxt
        
        self.createFrame()
        if self.text:
            self.createText()
        self.createEntry()
        self.createButtons()
        
    def createFrame(self):
        self.UIframe = Frame(self.master) #TODO: more specifications
        self.UIframe.pack()
        
    def createText(self):
        self.displayText = Label(self.UIframe, width=50, height=self.text.count("\n")+1, text=self.text)
        self.displayText.pack()
        
    def validate(self, action=None, index=None, value=None, priorValue=None, text=None, validationType=None, triggerType=None, widgetName=None):
        if value == None:
            return False
        elif " " in value:
            return False
        else:
            return True
        
        
    def createEntry(self):
        cmd = (self.master.register(self.validate), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")
        self.enterRoomName = Entry(self.UIframe, borderwidth=3, width=20, validate="key", validatecommand=cmd, takefocus=True)
        self.enterRoomName.focus_set()
        self.enterRoomName.insert("end", self.roomName)
        self.enterRoomName.pack(side="left", expand=True, fill="both")
    
    def createButtons(self):
        self.new = Button(self.UIframe, text="Generate room name", height=1, width=16, command=lambda:self.randRoom())
        self.new.pack(side="left", padx=3, pady=3)
        
        self.enter = Button(self.UIframe, text="Enter", height=1, width=8, command=self.processRoomName)
        self.enter.pack(side="left", padx=3, pady=3)
        
    def randRoom(self):
        randName = choice(ADVERBS) + "_" + choice(ADJECTIVES) + "_" + choice(NOUNS)
        if randName.startswith("_"):
            randName =  randName[1:]
        
        #don't use addValue, since it disables enterRoomName
        self.enterRoomName.delete(0, "end")
        self.enterRoomName.insert(0, randName)
        
    def processRoomName(self):
        self.roomName = self.enterRoomName.get()
        
        self.enter.config(relief="sunken") #button pressed
        response = self.net.post("create-room", room_name=self.roomName)
        
        if response["error"]:
            self.displayText.config(text="ERROR: " + response["error"])
            self.enter.config(relief="raised") #button unpressed
            
        else:
            self.currUsers = response["users"]
            self.UIframe.destroy()
            self.UIframe.quit()
        
    def saveSettings(self, settings, init=False):
        self.UIframe.configure(bg=colourConversion(settings.theme)["bg"]) #this doesnt seem to work?
        if self.text:
            self.displayText.configure(bg=colourConversion(settings.theme)["bg"], fg=colourConversion(settings.theme)["title"], font=(settings.font, settings.fontsize))
        
        self.enterRoomName.configure(font=(settings.font, settings.fontsize))
        print(settings.fontsize, type(settings.fontsize))
        self.new.configure(font=(settings.font, settings.fontsize), width=int(settings.fontsize)+8)
        self.enter.configure(font=(settings.font, settings.fontsize), width=int(settings.fontsize))
            
    def mainloop(self):
        self.UIframe.mainloop()

if __name__ == "__main__":
    from tkinter.ttk import Notebook
    from net import Net
    from helpers import loadToken
    net = Net()
    net.setToken(loadToken())
    
    root = Tk()
    notebook = Notebook(root, width=800, height=600)
    notebook.enable_traversal()
    notebook.pack()
    
    ##SECTION 1
    mainframe = Frame(notebook, bg="white", borderwidth=0, highlightthickness=0)
    notebook.add(mainframe, text="New Room")
    notebook.select(mainframe)
    
    gui = GetRoom(mainframe, net, "<enter room name>", text="hello user")
    gui.UIframe.mainloop()
    roomName = gui.roomName
    #print(roomName)
    
    #SECTION 2
    textbox = Entry(mainframe, width=100)
    textbox.pack()
    textbox.insert(0, "next section - display room and messages")
    root.mainloop()
        
