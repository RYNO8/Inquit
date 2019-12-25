from tkinter import Button, Entry, Label, PhotoImage, Tk
from random import choice
import os
import error

from helpers import runTask, addValue, colourConversion, LONG_ICON

__all__ = ["AuthUser"]

class AuthUser:
    def __init__(self, master, net, settings):
        self.master = master
        self.net = net
        self.settings = settings
        
        wH, wW = 450, 370
        sH, sW = self.master.winfo_screenheight(), self.master.winfo_screenwidth()
        self.master.geometry(str(wW) + "x" + str(wH) + "+" + str(sW//2-wW//2) + "+" + str(sH//2-wH//2))
        self.master.resizable(False, False)
        self.master.bind("<Return>", self.onEnter)
        self.master.tk_setPalette(background=colourConversion(self.settings.theme)["bg"])
        self.createLogo()
        self.step1()
        
    def createLogo(self):
        self.img = PhotoImage(file=LONG_ICON)
        self.label = Label(self.master, image=self.img, bg=colourConversion(self.settings.theme)["bg"])
        self.label.grid(row=0, columnspan=2, padx=30, pady=30)
    
    def step1(self):
        self.usernameLabel = Label(self.master, borderwidth=3, text="Username")
        self.usernameLabel.grid(row=1, column=0)
        
        self.passwordLabel = Label(self.master, borderwidth=3, text="Password")
        self.passwordLabel.grid(row=1, column=1)
        
        self.entryBox = Entry(self.master, borderwidth=3, takefocus=True, fg="#000000", bg="#EEEEEE")
        self.entryBox.insert("end", os.getlogin())
        self.entryBox.grid(row=2, column=0)
        
        self.passwordBox = Entry(self.master, borderwidth=3, fg="#000000", bg="#EEEEEE") #TODO: hide password
        self.passwordBox.grid(row=2, column=1)
        
        self.button = Button(self.master, text="Log in / Sign up", height=1, width=16, fg="#000000", bg="#EEEEEE", command=self.step2)
        self.button.grid(row=3, columnspan=2, pady=10, ipadx=40)
        
        self.errorBox = Label(self.master, text="", highlightcolor="red")
        self.errorBox.grid(row=4, columnspan=2)
        
        
    def step2(self):
        self.username = self.entryBox.get()
        self.password = self.passwordBox.get()
        if not self.username:
            self.errorBox.config(text="ERROR: missing username")
            return
        elif not self.password:
            self.errorBox.config(text="ERROR: missing password")
            return
        
        response = self.net.post("auth-user", username=self.username)
        #print(response)
        #response = {'error': None, 'question': 'whats 9+10?'}
        if response["error"] == "username already exists. Choose another":
            self.step4()
            return
            
        if not response or response["error"]:
            self.master.destroy()
            error.main(response["error"])
        
        else:
            self.usernameLabel.destroy() ; self.passwordLabel.destroy() ; self.passwordBox.destroy()
            self.errorBox.config(text="")
            self.entryBox.delete(0, "end")
            self.entryBox.grid(row=2, column=0, ipadx=20)
            
            self.button.configure(text="Submit answer", command=self.step3)
            self.button.grid(row=2, column=1, padx=20, ipadx=0)
            
            self.question = Label(self.master, borderwidth=3, text="(CAPTCHA verification)\n" + response["question"], takefocus=True)
            self.question.grid(row=1, columnspan=2, pady=10)
            
    def step3(self):
        self.answer = self.entryBox.get()
        if not self.answer:
            self.errorBox.config(text="ERROR: missing answer")
            return
        
        self.entryBox.delete(0, "end")
        
        response = self.net.post("register", username=self.username, password=self.password, answer=self.answer)
        #self.master.destroy()
        
        if not response or response["error"]:
            error.main(response["error"], 300, 300)
            
        self.step4()
        
    def step4(self):
        response = self.net.post("login", username=self.username, password=self.password)
        if response["error"]:
            self.master.destroy()
            error.main(response["error"], 300, 300)
            
        self.token = response["token"]
        self.master.destroy()
    
    def onEnter(self, press):
        self.button.invoke()
        
def main(net, settings):
    root = Tk()
    app = AuthUser(root, net, settings)
    root.mainloop()
    
    try:
        return app.username, app.password, app.token
    except AttributeError:
        return None, None, None
    
if __name__ == "__main__":
    from net import Net
    from helpers import loadPreferences, Settings
    net = Net()
    s = Settings(loadPreferences())
    s.theme = "dark"
    username, password, token = main(net, s)
    print(username, password, token)
        
