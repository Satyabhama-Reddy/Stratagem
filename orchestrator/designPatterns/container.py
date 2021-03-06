import docker
import time
import threading  
client = docker.from_env()
from pprint import pprint
"""
before this:
pull repo
port number of container within container
name of image
"""
import socket
def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port

class Container:
    def __init__(self,image,containerPort):
        port=get_free_tcp_port()
        try:
            container=client.containers.create(image,
                                      detach=True,
                                      ports={(str(containerPort)+'/tcp'): port}) # inside : outside
        except Exception as e:
            print(e)
            exit()
        self.id=container.id
        self.port=port
        self.container=container
        self.cpuUsage=None
        self.usageThread=None
        self.usageThreadStop=False
        self.requestCount=0
        print("Created",self.port)

    def destructor(self):
        #if not stopped stop
        # if(self.usageThread!=None):
            # self.usageThreadStop=True
            # print("stopping thread")
            # self.usageThread.join()
        self.container.stop()
        self.container.remove()
        print("Deleted",self.port)
    
    def start(self):
        self.container.start()
        self.getStats(self.usageThreadStopSet,False)
        self.usageThread = threading.Thread(target=self.getStats,args=(self.usageThreadStopSet,),daemon=True)
        self.usageThread.start()
        print("Started",self.port)
        #start container
        # pass

    def stop(self):
        # self.usageThread.stop()
        ### THREADING
        # self.stopThread = threading.Thread(target=self.stopping, daemon=True)
        # self.stopThread.start()
        # print("Stopping",self.port)
        ###
        self.container.stop()
        print("Stopped",self.port)
        #stop container
        # pass

    # def stopping(self):
    #     self.container.stop()
    #     print("Stopped",self.port)

    def usageThreadStopSet(self):
        # print(self.usageThreadStop)
        return self.usageThreadStop

    def getStats(self, check, threaded=True):
        while check!=True:
            try:
                stats = self.container.stats(stream=False)
                self.cpuUsage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
            except:
                pass
            # print(self.port, self.cpuUsage)
            if threaded==False:
                return
            time.sleep(1)
        return
"""
if __name__ == "__main__":
    c=Container()
    c.start()
    c.stop()
"""
