from helpers import runTask, addValue
import time
import threading

from notify import Notification

def getTag(displayName, username):
    if displayName == username:
        return "selfmsg"
    else:
        return "othermsg"

def receive(self, doNotify):
    runTask(_receive, self, doNotify)

def _receive(self, doNotify):
    #TODO: currently using rapid get requests, change to stream (using urllib)
    import time
    n = Notification(self.frame)
    msgArchive = []
    timeLimit = 0
    
    while threading.main_thread().isAlive():
        response = self.net.post("messages", room_name=self.roomName, time_limit=str(timeLimit))
        timeLimit = int(time.time() - 100) #back 100 seconds, so no recent messages will be missed
        
        if not response:
            print("ERROR", "no response")
            continue
        
        elif response["error"]:
            print("ERROR", response["error"])
            continue
        
        for thing in response["messages"]:
            username, message, timestamp = thing["user"], thing["data"], thing["time"]
            
            if (username, message, timestamp) not in msgArchive:
                tag = getTag(self.displayName, username)
                addValue(self.displayBox, "\n    " + " ".join(timestamp)) #, tag="time")
                addValue(self.displayBox, "\n" + username + ": " + message + "\n", tag=tag)
                self.displayBox.see("end") #scroll to the bottom
                        
                #conditions for sending notifications
                if timeLimit != 0 and tag == "othermsg" and self.doNotify and not self.focus:
                    n.notify(username + ": " + decodedMessage, self.roomName)
                    
                msgArchive.append((username, message, timestamp))
                
        
                
        
def sendMsg(net, inputBox, roomName):
    runTask(_sendMsg, net, inputBox, roomName)

def _sendMsg(net, inputBox, roomName):
    text = inputBox.get()
    inputBox.delete(0, "end")
    if text.strip() == "":
        return ""
    
    response = net.post("send", room_name=roomName, message=text)
    
    # put bots here:
    for bot in [BotTheGame, BotTemplate]:
        bot(net, text, roomName)
    
    return text
    
def BotTheGame(net, text, roomName):
    botName = "The Game Bot"
    if "game" in text:
        response = net.post("send", room_name=roomName, message="Did someone say the game?")

def BotTemplate(net, text, roomName):
    """\
net - network class used to send msg
text - most recent text message sent
roomName - room (no spaces)
NOTE: there is no need to do threading. should enforce maximum time of 1s"""
    # do processing
    #net.post("send", room_name=roomName, "Message from the Bot")
    
if __name__ == "__main__":
    from net import Net
    from tkinter import Tk
    from tkinter.scrolledtext import ScrolledText
    """inputBox = Entry(root, borderwidth=2, takefocus=True, width=5, thread=True)
    inputBox.pack()
    inputBox.insert(0, "text")
    
    root.after(200, lambda :sendMsg(inputBox, "roomName", "Ryan", net))
    """

    class self:
        master = Tk()
        displayBox = ScrolledText(master)
        displayBox.pack()
        
        net = Net()
        roomName = "a"
        focus = False
        
        
    obj = self()
    runTask(receive, obj, True, "Ryan")
    obj.master.mainloop()
    
               
