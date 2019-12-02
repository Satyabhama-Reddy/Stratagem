from abc import ABC, abstractmethod

"""
Usage:
- Import both ContainerCountObservable and Observer
- Create the count value using the ContainerCountObservable
- Make the orchestrator a derive from observer
- Define an update function that takes the current state as a parameter
"""

class Observable():
    def __init__(self):
        self._state = 0
        self._observers = set()

    def subscribe(self, observer):
        observer._observable = self
        self._observers.add(observer)
        self.notify()

    def unsubscribe(self, observer):
        observer._observable = None
        self._observers.discard(observer)

    def notify(self):
        for observer in list(self._observers):
            observer.update(self._state)

    def getState(self):
        return self._state

    def setState(self, val):
        self._state = val
        self.notify()

    state = property(getState, setState)

class Observer(ABC):
    def __init__(self):
        self._observable = None

    @abstractmethod
    def update(self, arg):
        pass
