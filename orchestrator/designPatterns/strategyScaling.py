from abc import ABC, abstractmethod
import random
from orchestratorExceptions import *
from observer import Observer

class ScalingContext():
	def __init__(self, strategy, containers):
		self.setStrategy(strategy)

	def setStrategy(self, strategy):
		strategy=self.validate(strategy,containers)
		if strategy!=False:
			self.strategy = strategy
		else:
			raise InvalidScalingChoice

	def validate(self,strategy):
		if("strategy" not in strategy.keys()):
			return False
		if(strategy["strategy"]=="no scaling"):
			return NoScaling(containers)
		if(strategy["strategy"]=="request load"):
			if("numberOfRequests" not in strategy.keys() or "perDuration" not in strategy.keys()):
				return False
			if(type(strategy["numberOfRequests"])!=int or type(strategy["perDuration"])!=int):
				return False
			else:
				return RequestLoad(containers,requests,duration)

	def scale(self):
		self.strategy.scale()

class StrategyScaling(ABC):
	@abstractmethod
	def scale(self):
		pass

class NoScaling(StrategyScaling):
	def __init__(self, containers):
		self._containers = containers
	def scale(self):
		pass

class RequestLoad(StrategyScaling):
	def __init__(self, containers,requests,duration):
		self._containers = containers
		self._requests = requests
		self._duration = duration
	def scale(self):
		pass
