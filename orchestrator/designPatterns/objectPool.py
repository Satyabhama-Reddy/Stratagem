from container import Container
# from activeContainers import ActiveContainers

"""
Usage:
- Import ContainerPool
- pass minimum number of containers needed
"""

"""
Reference:
from objectPool import ContainerPool

if __name__=="__main__":
    minNoOfContainers = 3
    maxNoOfContainers = 6
    pool = ContainerPool(minNoOfContainers,maxNoOfContainers)
    container = pool.acquire()
    pool.release(container)
"""

class ContainerPool:
    def __init__(self, minContainers, maxContainers):
        self._inactiveContainers = [Container() for _ in range(minContainers)]
        self._activeContainers = []
        self._minContainers = minContainers
        self._maxContainers = maxContainers

    def acquire(self):
        container = self._inactiveContainers.pop()
        if(len(self._inactiveContainers) == 0 and len(self._activeContainers) < self._maxContainers):
            self.add(1)
            #when to delete?
        container.start()
        self._activeContainers.append(container)
        return container

    def release(self, container):
        # how to decide which container to release..?
        # if i pop the last container in active containers..that might be serving requests
        container.stop()
        self._activeContainers.remove(container)
        self._inactiveContainers.append(container)
    
    #additional functions that we need for scaling up/down that are not part of object pool design pattern

    def add(self, noOfAdditionalContainers):
        for i in range(noOfAdditionalContainers):
            self._inactiveContainers.append(Container())
        

    def delete(self, noOfContainers):
        # if the object is in the list then it is not being used as acquire pops it
        # so we need not worry about it being in the middle of a task
        for i in range(noOfContainers):
            obj = self._inactiveContainers.pop()
            del obj
