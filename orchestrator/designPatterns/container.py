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
    def __init__(self,image='flaskexample/flaskexample',containerPort=5000):
        port=get_free_tcp_port()
        container=client.containers.create(image,
                                      detach=True,
                                      ports={(str(containerPort)+'/tcp'): port}) # inside : outside
        self.id=container.id
        self.port=port
        self.container=container
        self.cpuUsage=None
        self.usageThread=None
        print("Created",self.port)

    def __del__(self):
        #if not stopped stop
        self.container.stop()
        self.container.remove()
        print("Deleted",self.port)
    
    def start(self):
        self.container.start()
        self.getStats(False)
        self.usageThread = threading.Thread(target=self.getStats, daemon=True)
        self.usageThread.start()
        print("Started",self.port)
        #start container
        # pass

    def stop(self):
        # self.usageThread.stop()
        self.container.stop()
        print("Stopped",self.port)

        #stop container
        # pass

    def getStats(self, threaded=True):
        while True:
            container=client.containers.list(filters={'id':self.id})[0]
            stats = container.stats(stream=False)
            self.cpuUsage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
            if threaded==False:
                return
            time.sleep(10)
"""
if __name__ == "__main__":
    c=Container()
    c.start()
    c.stop()
"""
