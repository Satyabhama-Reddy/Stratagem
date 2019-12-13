from abc import ABC, abstractmethod
import random
from orchestratorExceptions import *
from observer import Observer
import threading
import time 

class ScalingContext():
	def __init__(self, strategy, containers):
		self._containers = containers
		self.setStrategy(strategy)
		self.scale()		

	def setStrategy(self, strategy):
		strategyObject=self.validate(strategy,self._containers)
		if strategyObject!=False:
			self.strategy = strategyObject
			self.strategyDetails = strategy
			if("perDuration" not in self.strategyDetails.keys()):
				self.strategyDetails["perDuration"]=10
		else:
			raise InvalidScalingChoice

	def validate(self,strategy,containers):
		if("strategy" not in strategy.keys()):
			return False
		if(strategy["strategy"]=="no scaling"):
			return NoScaling(containers)
		if(strategy["strategy"]=="request load"):
			if("numberOfRequests" not in strategy.keys() or "perDuration" not in strategy.keys()):
				return False
			if(type(strategy["numberOfRequests"])!=int or type(strategy["perDuration"])!=int):
				return False
			if(strategy["numberOfRequests"]<=0 or strategy["perDuration"]<=0):
				return False
			else:
				return RequestLoad(containers,strategy["numberOfRequests"],strategy["perDuration"])

	def scale(self):
		thread = threading.Thread(target=self.scaleManager,daemon=True)
		thread.start()

	def scaleManager(self):
		while(1):
			self.strategy.scale()
			time.sleep(self.strategyDetails["perDuration"])
			

	def increment(self):
		self.strategy.increment()

class StrategyScaling(ABC):
	@abstractmethod
	def scale(self):
		pass
	@abstractmethod
	def increment(self):
		pass

class NoScaling(StrategyScaling):
	def __init__(self, containers):
		self._containers = containers
	def scale(self):
		# print("scaling")
		pass
	def increment(self):
		pass

class RequestLoad(StrategyScaling):
	def __init__(self, containers,requests,duration):
		self._containerPool = containers
		self._requests = requests
		self._duration = duration
		self._requestsInPreviousDuration = 0
	def scale(self):
		scaleTo = int(self._requestsInPreviousDuration/self._requests)
		if(scaleTo==0):
			scaleTo=1
		current = self._containerPool.numberContainers.state
		print("Scaling : ",current,"(",scaleTo-current,")",sep="")
		i=0
		if(scaleTo>current):
			while(i<(scaleTo-current)):
				self._containerPool.acquire()
				i+=1
		elif(scaleTo<current):
			while(i<(current-scaleTo)):
				container = self._containerPool.getFreeContainer()
				if(container==None):
					break
				self._containerPool.release(container)
				i+=1
		# print("number of containers needed :",scaleTo)
		# print("number of containers present :",len(self._containerPool))
		self._requestsInPreviousDuration = 0
	def increment(self):
		self._requestsInPreviousDuration +=1
