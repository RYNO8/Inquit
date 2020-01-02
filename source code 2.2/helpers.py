import threading
import concurrent.futures
import base64
import inspect
import os
import pickle
from datetime import datetime
from dateutil import tz
import sys
import platform

__all__ = ["LONG_ICON", "SHORT_ICON", "IS_WINDOWS", "CURR_VERSION", "SETTINGS_FILE", "SSID_FILE", "MASTER_KEY", "DEFAULT",
           "getFILEPATH", "getFILENAME", "runThread", "runTask", "formatTime", "addValue", "addImage", "colourConversion",
           "Settings", "loadPreferences", "savePreferences", "loadSSID", "saveSSID"]

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

LONG_ICON = resource_path(".img\\Inquit_Icon_Long.png") #DONT change this
SHORT_ICON = resource_path(".img\\Inquit_Icon.ico") #or this
IS_WINDOWS = (platform.system() == "Windows")
CURR_VERSION = 2.2
SETTINGS_FILE = "preferences.txt"
SSID_FILE = "SSID.txt"
TOKEN_FILE = "token.txt"
DEFAULT = {"font":"Consolas",
           "fontsize":11,
           "displayName":"",
           "token":"",
           "theme":"light",
           "notify":"1",
           "prevRoom":"",
           }

def getFILEPATH():
    return os.path.dirname(os.path.abspath(getFILENAME()))

def getFILENAME():
    return inspect.getframeinfo(inspect.currentframe()).filename

def runThread(func, *args, **kwargs):
    """WARNING: errors will pass unnoticed"""
    executor = concurrent.futures.ThreadPoolExecutor()
    future = executor.submit(func, *args, **kwargs)
    return future.result

def runTask(func, *args, **kwargs):
    thread = threading.Thread(target=func, daemon=True, args=args, kwargs=kwargs)
    thread.start()

def addValue(textbox, text, tag=""):
    textbox.config(state="normal")
    textbox.insert("end", text, tag)
    textbox.config(state="disabled")

def addImage(textbox, img, tag=""):
    #textbox.config(state=NORMAL)
    #textbox.image_create(END, image=image)
    imageLabel = Label(image=img)
    textbox.window_create("end", window=imageLabel)
    #textbox.config(state=DISABLED)

def colourConversion(themename):
    if themename == "light":
        #colour = {"bg":"#EEEEEE", "border":"#EEEEEE",  "own":"#039BE5", "other":"#006834", "title":"green"}
        colour = {"bg":"#EEEEEE", "border":"#EEEEEE",  "own":"#039BE5", "other":"#0082b3", "title":"purple"}
    elif themename == "dark":
        #colour = {"bg":"#36393F", "border":"#36393F",  "own":"#4DD0E1", "other":"#9CCC65", "title":"#C3759B"}
        colour = {"bg":"#36393F", "border":"#36393F",  "own":"#4DD0E1", "other":"#00d9ff", "title":"#e47df2"}
    else:
        raise Exception("unknown: " + themename)
    return colour

def settingsToDict(settings):
    return {attr:settings.__getattr__(attr) for attr in settings.__dir__() if not attr.startswith("__")}

class Settings:
    def __init__(self, data):
        if isinstance(data, dict):
            pass #data = data
        
        elif isinstance(data, Settings):
            data = settingsToDict(data)
        else:
            raise TypeError("must be type dictionary or Settings, not " + type(data).__name__)
        
        for k, v in data.items():
            self.__setattr__(k, v)
            
    def __getattr__(self, attr):
        if attr in self.__dir__():
            return eval("self." + attr)
        else:
            raise AttributeError("'Settings' object has no attribute " + attr)
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return str(settingsToDict(self))
    
    def __iter__(self):
        for attr in self.__dir__():
            if not attr.startswith("__"):
                yield attr, self.__getattr__(attr)
        
def loadPreferences(roomName=""):
    try:
        settings = pickle.load(open(SETTINGS_FILE, "rb"))
    except FileNotFoundError:
        settings = Settings(DEFAULT.copy())
        savePreferences(settings)
    return settings

def savePreferences(settings):
    assert isinstance(settings, Settings)
    pickle.dump(settings, open(SETTINGS_FILE, "wb"))

def loadSSID():
    try:
        with open(SSID_FILE, "r") as f:
            return [i.strip() for i in f.readlines()]
        
    except FileNotFoundError:
        saveSSID("") #to create the file
        return []

def saveSSID(data):
    with open(SSID_FILE, "w") as f:
        f.write("""\
add your school SSID below to be registered as "at school", to enable Inquit to bypass the proxy
e.g.
sbhs
McDonalds Free WiFi
""")
        
        for line in data:
            f.write(line)
            f.write("\n")

if __name__ == "__main__":
    a = Settings({"a":1})
    a = Settings(a)
