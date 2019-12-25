import _wifissid as wifissid
from string import whitespace
import urllib.request
from urllib import parse
from helpers import runThread, loadSSID, runTask
import time

#GOT URLLIB SESSION?

__all__ = ["validData", "getNetStatus", "Net"]

SCHOOL_SSID_LIST = ["Ascham BYOD Onboard", "sbhs", "NSBHS", "COLGINTERNAL", "STCBYOD"]
SCHOOL_SSID_LIST.extend(loadSSID())
DOMAIN = "https://1ype7i6i62.execute-api.ap-southeast-2.amazonaws.com/inquit/"
VERSION_CHECK_URL = "https://github.com/RYNO8/Inquit/blob/master/README.md"
GET_ENDPOINTS = ["ping"]
POST_ENDPOINTS = ["auth-user", "register", "login", "create-room", "invite", "send", "messages"]

#error has to do with the following code
def validData(data):
    return all([isinstance(i, str) and i not in whitespace for i in data.values()]) and "key" not in data.keys()

def getNetStatus():
    SSID = wifissid.showssid()
    isConnected = (SSID != "None")
    atSchool = True if SSID in SCHOOL_SSID_LIST else False
    return isConnected, atSchool

class Net:
    def __init__(self):
        """network for get requests with amazom lambda REST API request. initiates self.isConnected, self.SSID, self.net"""
        self.isConnected, self.atSchool = getNetStatus()
        self._token = None
        
        if self.atSchool:
            #print("at school")
            urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({'http': 'http://:@proxy.intranet:8080', 'https': 'http://:@proxy.intranet:8080'})))
        
    def ping(self):
        """returns connection time im ms. threading is not supported"""
        start = time.time()
        response = self.get("ping")
        duration =  (time.time() - start) * 1000
        assert response == "pong"
        return duration
    
    def get(self, uri):
        #TODO: test this
        assert uri in GET_ENDPOINTS
        
        if thread:
            return runThread(self.get, uri)
        url = DOMAIN + uri
        
        try:
            response = eval(urllib.request.urlopen(req).read().decode())
            return response
        except Exception as e:
            print("network GET error:", e)
            return None
        
    def getT(self, uri):
        return runThread(self.post, uri)
    
    def post(self, uri, **data):
        #TODO: test this
        assert uri in POST_ENDPOINTS
        assert "thread" not in data
        assert "token" not in data
        
        if self._token:
            data["token"] = self._token
        
        url = DOMAIN + uri.strip("/") + "?" + "&".join([k + "=" + parse.quote(str(v)) for k, v in data.items()])
        #print(url)
        req = urllib.request.Request(url, data={})
        
        try:
            response = eval(urllib.request.urlopen(req).read().decode())
            #print(response)
            return response
        except Exception as e:
            print("network POST error:", e)
            return None
        
    def postT(self, uri, **data):
        return runThread(self.post, uri, **data)
    
    def stream(self, room):
        #TODO: implement this
        pass
        
    def getVersion(self):
        response = urllib.request.urlopen(VERSION_CHECK_URL).read().decode()
        return float(response.partition("Current version: ")[2].partition("</p>")[0])
    
    def setToken(self, token):
        assert isinstance(token, str)
        self._token = token
        
    @property
    def token(self):
        return self._token
    
if __name__ == "__main__":
    from helpers import runThread
    
    net = Net()
    #print(net.getVersion())
    #print(net.ping())
    print(net.post("auth-user", username="R y a n"))
    
