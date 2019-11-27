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
    pool = ContainerPool(minNoOfContainers)
    container = pool.acquire()
    pool.add(2)
    pool.delete(3)
    pool.release(container)
"""

class ContainerPool:
    def __init__(self, noOfContainers):
        self._containers = [Container() for _ in range(noOfContainers)]

    def acquire(self):
        container = self._containers.pop()
        container.start()
        return 

    def release(self, container):
        # when release is called we need to make sure that the container is not servicing any requests
        container.stop()
        self._containers.append(container)
    
    #additional functions that we need for scaling up/down that are not part of objec tpool design pattern

    def add(self, noOfAdditionalContainers):
        for i in range(noOfAdditionalContainers):
            self._containers.append(Container())
        

    def delete(self, noOfContainers):
        # if the object is in the list then it is not being used as acquire pops it
        # so we need not worry about it being in the middle of a task
        for i in range(noOfContainers):
            obj = self._containers.pop()
            del obj
        


class Container:
    def __init__(self):
        #create docker image
        #self id = id
        #state?
        print("Container created")

    def __del__(self):
        #delete docker image
        print("Container deleted")
    
    def start(self):
        #start container
        pass

    def stop(self):
        #stop container
        pass

