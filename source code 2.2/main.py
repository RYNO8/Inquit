import auth_user
import error
import gui
import helpers
import loading
import net as n

from tkinter import Tk

settings = helpers.loadPreferences()
net = n.Net()

success, text = loading.main(net, settings)
#success, text = True, "2.1: Welcome developer."

if not success:
    error.main(text)
    
else:
    if not settings.token:
        settings.displayName, password, settings.token = auth_user.main(net, settings)
    
    if settings.token and settings.displayName:
        helpers.savePreferences(settings)
        net.setToken(settings.token)
        
        root = Tk()
        inquit = gui.Inquit(root, net, settings, text=text, state="")
        
        root.mainloop()

helpers.savePreferences(settings)
print("saved")
