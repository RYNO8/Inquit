import zroya
import os
from helpers import runThread, runTask, SHORT_ICON
from copy import deepcopy
import time

#TODO:: zroya.hide(id) not working

class Notification:
    def __init__(self, window):
        #self.notify = deepcopy(self.notifyMac)
        self.roomName = ""
        self.shouldShow = False
        self.window = window
        self.window.after(200, self.checkShow)
        
    def notify(self, *args):
        runThread(self.notifyWindows, *args)
        
    def notificationHandler(self, *args):
        #BIG WARNING: errors do not show up
        buttonId = args[-1]
        
        if len(args) > 1 and args[1] == 0: #Show Message
            self.shouldShow = True
            
        else: #Yeet Message Away
            pass

    def notifyWindows(self, message, roomName):
        self.roomName = roomName
        zroya.init(roomName, "Inquit", "Inquit", "Inquit", "2.1")
        template = zroya.Template(zroya.TemplateType.ImageAndText4)
        template.setFirstLine("Inquit")
        template.setSecondLine(message)
        template.setAttribution("By Ryan O and Nathan J")
        template.setImage(SHORT_ICON)
        template.addAction("Show Message")
        template.addAction("Yeet Message Away")
        
        notificationID = zroya.show(template, on_click=self.notificationHandler, on_action=self.notificationHandler)
        print(notificationID)
        
    def notifyMac(window, message, roomName):
        os.system("osascript -e \'display notification \"Inquit\" with title \"" + message + "\" from room \"" + roomName + "\" \'")

    def checkShow(self):
        if self.shouldShow:
            window.focus_force()
            self.shouldShow = False
            
        self.window.after(200, self.checkShow)
        
if __name__ == "__main__":
    import tkinter
    window = tkinter.Tk()
    n = Notification(window)
    try:
        n.notify("hello", "roomwName")
    except Exception as e:
        print(e)
        print(e.__traceback__(), e.with_traceback.__dir__())
