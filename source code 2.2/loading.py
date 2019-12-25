from tkinter import Tk, Button, Frame, Label, PhotoImage, Text, HORIZONTAL, DISABLED, BOTH
from tkinter.ttk import Progressbar
from random import choice
import time

from helpers import runTask, addValue, colourConversion, LONG_ICON, SHORT_ICON, CURR_VERSION, DEBUG_MODE
from custom_widgets import HyperlinkManager
from net import Net



class Loading:
    def __init__(self, master, net, settings):
        self.master = master
        self.net = net
        
        self.JOKE_SUBMIT = "https://docs.google.com/forms/d/e/1FAIpQLSeYeU-fs-ky2M9gx05fjgiH0yi68dwgJmD6WsUvFj9Vfc5CUQ/viewform?usp=sf_link"
        self.jokes = ["Why did the cow cross the road?\nTo get to the udder side.", 
                      "Your mum",
                      "Have you heard about the Italian Chef?\nHe pasta way.",
                      "Have you heard about the Italian Chef?\nHe pasta way.",
                      "Have you heard of the Italian chef? \nHe ran out of thyme.",
                      "Have you heard of the Italian chef? \nI never sausage a terrible thing.",
                      "No swearing on the ground.",
                      "Rhythm Nath want to say:\nWhat do you call a chicken staring at lettuce?\nA chicken caesar.",
                      "I lost the game!", 
                      "Why did the chicken cross the road? idk",
                      "Do you guys want to hear another joke? My life lol xd",
                      "If the petrol station is 2km away from my house, and if the average \nmale walks at about 5km/hour then why has it taken my Dad 10 years to \nget back from the petrol station?",
                      "What's the difference between a priest and acne? Acne waits until the boy is twelve to come on his face",
                      "Ben: knock knock\nJames: Who is at the door ben?\nBen: I\nJames: I? I who?\nBen: I hate minority groups",
                      "Why can't you hear a pterodactyl pee? \nBecause theyre dead",
                      "Where did Lucy go during the bombing? \nEverywhere",
                      "99 bugs in the code... 99 bugs in the code, 99 bugs in the code! Take one down, patch it around. 127 bugs in the code.",
                      "Time flies like the wind. Fruit flies like a banana!",
                      "Ya mum",
                      "I have aidez",
                      "Where did the grass eat? Out.",
                      "What are 10^-12 choos? Pikachus!",
                      "Adversity has the effect of eliciting talents, which in prosperous circumstances would have lain dormant.",
                      "I dunno if he's gay or not \nbut you know what they say \na fortnite farmer's a fortnite farmer",
                      "The addiction helpline cannot help you on Sundays. \nSo, just don't have an addiction on Sunday."]
        
        wH, wW = 260, 600
        sH, sW = self.master.winfo_screenheight(), self.master.winfo_screenwidth()
        self.master.geometry(str(wW) + "x" + str(wH) + "+" + str(sW//2-wW//2) + "+" + str(sH//2-wH//2))
        self.master.resizable(False, False)
        
        self.createProgress()
        self.createBox()
        
        runTask(self.logic)
        self.master.after(200, self.checkClose)
        self.master.after(1, lambda: self.saveSettings(settings))
        
    def checkClose(self):
        try:
            self.success, self.text
        except:
            pass
        else:
            self.master.destroy()
        self.master.after(200, self.checkClose)
        
    def createProgress(self):
        self.img = PhotoImage(file=LONG_ICON)
        self.label = Label(self.master, image=self.img)
        self.label.pack()
        
        self.progress = Progressbar(self.master, orient=HORIZONTAL, length=self.img.width()-50, mode="indeterminate")
        self.progress.pack()
        self.progress.start()
        
    def createBox(self):
        self.textbox = Text(self.master, state=DISABLED, relief="flat")
        self.textbox.pack(expand=True, fill="both", padx=6, pady=6) #TODO: scroll=False
        hyperlink = HyperlinkManager(self.textbox)
        
        joke = choice(self.jokes)
        addValue(self.textbox, joke + "\n\n", tag="title")
        addValue(self.textbox, "click here to submit a random message\n\n", (*hyperlink.add(self.JOKE_SUBMIT), "comment"))
        
    def logic(self):
        if DEBUG_MODE:
            time.sleep(0.1)
        else:
            time.sleep(2)
        self.success, self.text = reportVersion(self.net)
        
    def saveSettings(self, settings):
        self.master.configure(bg=colourConversion(settings.theme)["bg"])
        self.label.configure(bg=colourConversion(settings.theme)["bg"])
        self.textbox.configure(bg=colourConversion(settings.theme)["bg"])
        self.textbox.configure(font=(settings.font, settings.fontsize))
        self.textbox.tag_configure("title", foreground=colourConversion(settings.theme)["title"])
        self.textbox.tag_configure("comment", foreground=colourConversion(settings.theme)["own"])
    
def reportVersion(net):
    if not net.isConnected:
        return False, "No Internet For You\n¯\_(ツ)_/¯  ¯\_(ヅ)_/¯  ¯\_(ツ)_/¯\n"
    
    newest_version = net.getVersion()
    if newest_version > CURR_VERSION:
        return False, str(CURR_VERSION) + ": This version is out of date. \n\nVisit https://github.com/RYNO8/Inquit \nfor the newest version\n"
        
    elif newest_version == CURR_VERSION:
        return True, str(CURR_VERSION) + ": This version is up to date\n"
        
    elif newest_version < CURR_VERSION: #version not released yet
        return True, str(CURR_VERSION) + ": Welcome developer.\n"


def main(net, settings):
    root = Tk()
    root.title("Loading")
    app = Loading(root, net, settings)
    root.mainloop()
    try:
        return app.success, app.text
    except AttributeError:
        return None, "Abrupt User Exit"

if __name__ == "__main__":
    from helpers import Settings, loadPreferences
    s = Settings(loadPreferences())
    #s.fontsize = 3
    s.theme = "dark"
    success, text = main(Net(), s)
    print(success, text)


