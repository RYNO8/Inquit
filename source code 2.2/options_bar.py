from tkinter import Button, Entry, Frame, Label, Text, Toplevel, Tk
from tkinter.ttk import Combobox
from helpers import addValue, DEFAULT
from custom_widgets import HyperlinkManager

__all__ = ["windowTemplate", "showAboutMenu", "showHelpMenu", "customise"]

MAIN_PAGE = "https://github.com/RYNO8/Inquit"
ISSUES_PAGE = "https://github.com/RYNO8/Inquit/issues"
BUGS_PAGE = "https://github.com/RYNO8/Inquit/issues"

def windowTemplate(master, title, width, height):
    menu = Toplevel(master)
    menu.title(title)
    menu.resizable(False, False)
    menu.lift(aboveThis=master)
    menu.focus_force()
    
    frame = Frame(menu)
    frame.pack(fill="both", expand="yes", padx=3, pady=3, anchor="nw")
    
    textBox = Text(frame, width=width, height=height, state="disabled")
    textBox.pack()
    return menu, frame, textBox

def showAboutMenu(master):
    aboutMenu, frame, textBox = windowTemplate(master, "About", 100, 15)
    hyperLink = HyperlinkManager(textBox)
    addValue(textBox, """\n
 Version: 2.2
 by Ryan O and Nathan J
 Made in python (3.7.2 64 bit AMD64) using tkinter
 FOUND A BUG? """)
    addValue(textBox, "look here\n", hyperLink.add(BUGS_PAGE))
    addValue(textBox, " HAVE A SUGGESTION? ")
    addValue(textBox, "look here\n", hyperLink.add(ISSUES_PAGE))
    addValue(textBox, """\n\nCheck out """)
    addValue(textBox, "my github page", hyperLink.add(MAIN_PAGE))
    addValue(textBox, """ for newer versions.""")
    
    b = Button(master=frame, text="OK", padx=3, pady=3, height=1, width=7, command=aboutMenu.destroy)
    b.pack(side="bottom")
    
    aboutMenu.mainloop()
    aboutMenu.quit()
        
def showHelpMenu(master):
    helpMenu, frame, textBox = windowTemplate(master, "Help", 50, 7)
    addValue(textBox, "Yes. You need help\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n I LOST THE GAME.\n :)\n")
    
    b = Button(master=frame, text="Yes I know", padx=3, pady=3, height=1, width=11, command=helpMenu.destroy)
    b.pack(side="bottom")
    
    helpMenu.mainloop()
    helpMenu.quit()

def insertOption(master, settings, rowNum, text):
    label = Label(master, text=text, font=(settings.font, settings.fontsize))
    label.grid(column=0, row=rowNum, sticky="w")

def customise(master, settings, save, WIDTH=30):
    customiseMenu = Toplevel()
    customiseMenu.title("Settings")
    customiseMenu.resizable(False, False)
    customiseMenu.lift(aboveThis=master)
    customiseMenu.focus_force()
    
    frame = Frame(customiseMenu)
    frame.pack(fill="both", expand="yes", padx=3, pady=3, anchor="nw")
    
    for rowNum, option in enumerate(["Username: ", "Theme: ", "Font: ", "Font size: ", "Allow notifications: "]):
        insertOption(frame, settings, rowNum, option)
    
    #row=0 (Username)
    displaynameBox = Entry(frame, width=WIDTH, font=(settings.font, settings.fontsize))
    displaynameBox.insert("end", settings.displayName)
    displaynameBox.grid(column=1, row=0)
    
    #row=1 (Theme)
    themeBox = Combobox(frame, width=WIDTH-3, font=(settings.font, settings.fontsize), state="readonly")
    themeBox["values"] = ["light", "dark"]
    themeBox.current(themeBox["values"].index(settings.theme))
    themeBox.grid(column=1, row=1)
    
    #row=2 (Font)
    fontBox = Entry(frame, width=WIDTH, font=(settings.font, settings.fontsize))
    fontBox.insert("end", settings.font)
    fontBox.grid(column=1, row=2)
    
    #row=3 (Font Size)
    fontsizeBox = Entry(frame, width=WIDTH, font=(settings.font, settings.fontsize))
    fontsizeBox.insert("end", settings.fontsize)
    fontsizeBox.grid(column=1, row=3)
    
    #row=4 (Allow Notifications)
    notifyChoices = {"yes":"1", "no":"0"}
    notifyBox = Combobox(frame, width=WIDTH-3, font=(settings.font, settings.fontsize), values=list(notifyChoices.keys()), state="readonly")
    notifyBox.current(0)
    notifyBox.grid(column=1, row=4)
    
    def getSettings():
        newSettings = {"font":fontBox.get(),
                       "fontsize":fontsizeBox.get(),
                       "displayName":displaynameBox.get(),
                       "theme":themeBox.get(),
                       "notify":notifyChoices[notifyBox.get()],
                       }
        #print(settings)
        save({**dict(settings), **newSettings})
        customiseMenu.destroy()
    
    def resetSettings():
        newSettings = dict(settings)
        for key in newSettings:
            if DEFAULT[key]:
                newSettings[key] = DEFAULT[key]
        
        save(newSettings)
        customiseMenu.destroy()
    
    #Reset Button
    resetButton = Button(frame, text="Reset", padx=0, pady=0, height=1, width=25, command=resetSettings)
    resetButton.grid(column=0, row=5)
    
    #Apply Button
    applyButton = Button(frame, text="Apply", padx=0, pady=0, height=1, width=25, command=getSettings)
    applyButton.grid(column=1, row=5)

if __name__ == "__main__":
    from helpers import runTask, runThread, loadPreferences, Settings
    
    settings = Settings(loadPreferences(roomName="")) #{"font":"Consolas", "fontsize":11, "display_name":"Ryan", "theme":"light", "notify":"1",}
    
    root = Tk()
    runThread(showAboutMenu, root)
    runThread(showHelpMenu, root)
    customise(root, settings, lambda _:None) #runThread(customise, root)
