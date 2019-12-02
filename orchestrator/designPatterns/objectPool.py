from container import Container

"""
Usage:
- Import ContainerPool
- pass minimum number of containers needed
"""

class ContainerPool:
    def __init__(self, minContainers, maxContainers):
        self._inactiveContainers = [Container() for _ in range(minContainers)]
        self._activeContainers = []
        self._minContainers = minContainers
        self._maxContainers = maxContainers
        self.count = 0

        for containerInd in range(self._minContainers):
            self.acquire()
    
    def acquire(self):
        if(len(self._inactiveContainers)==0):
            return -1
        container = self._inactiveContainers.pop()
        if(len(self._inactiveContainers) == 0 and len(self._activeContainers) < self._maxContainers):
            self.add(1)
            #when to delete?
        container.start()
        self._activeContainers.append(container)
        self.count+=1
        return container

    def release(self, container):
        # how to decide which container to release..?
        # if i pop the last container in active containers..that might be serving requests
        container.stop()
        self._activeContainers.remove(container)
        self._inactiveContainers.append(container)
        self.count-=1

    
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

    def __iter__(self):
        return ContainerIterator(self._activeContainers)

    def __len__(self):
        return len(self._activeContainers)

    def __getitem__(self, key):
        return self._activeContainers[key]

class ContainerIterator():
    def __init__(self, activeContainers):
        self._activeContainers = activeContainers
        self._cursor = 0

    def __next__(self):
        try:
            nextContainer = self._activeContainers[self._cursor] 
            self._cursor+=1
            return nextContainer
        except:
            raise StopIteration

"""
if __name__=="__main__":
    minNoOfContainers = 3
    maxNoOfContainers = 6
    pool = ContainerPool(minNoOfContainers,maxNoOfContainers)
    container = pool.acquire()
    container.getStats()
    container = pool.acquire()
    container = pool.acquire()
    container = pool.acquire()
    pool.release(container)
"""