from helpers import addValue, Settings, colourConversion, LONG_ICON, DEFAULT

from tkinter import Toplevel, Frame, Text, PhotoImage, Label
import sys

__all__ = ["main"]

def main(errorMsg, wH=300, wW=400):
    """BIG NOTE: make sure all windows are destroy() before running this"""
    settings = globals().get("settings", Settings(DEFAULT))
    
    #the following is basically the same as options_bar.windowTemplate, but without requiring a first window
    root = Toplevel()
    root.tk_setPalette(background=colourConversion(settings.theme)["bg"])
    root.title("Inquit - Error")
    sH, sW = root.winfo_screenheight(), root.winfo_screenwidth()
    root.geometry(str(wW) + "x" + str(wH) + "+" + str(sW//2-wW//2) + "+" + str(sH//2-wH//2))
    root.resizable(False, False)
    
    def destroy():
        root.destroy()
        #print("destroying")
        sys.exit()
    
    root.protocol("WM_DELETE_WINDOW", destroy)
    
    frame = Frame(root)
    frame.pack(fill="both", expand="yes", padx=3, pady=3, anchor="nw")
    
    photo = PhotoImage(file=LONG_ICON)
    #print(type(photo))
    label = Label(frame, image=photo)
    label.image = photo # keep a reference!
    label.pack(side="top")
    
    textBox = Text(frame, width=10000, height=10000, state="disabled", relief="flat", font=(settings.font, settings.fontsize))
    textBox.tag_configure("center", justify='center')
    textBox.pack(padx=8, pady=8)
    addValue(textBox, errorMsg, tag="center")
    root.mainloop()
    

if __name__ == "__main__":
    from helpers import loadPreferences
    globals()["settings"] = Settings(loadPreferences())
    #globals()["settings"].theme = "dark"
    
    main("Oh no. I lost the game. \nI must self-destruct now")
