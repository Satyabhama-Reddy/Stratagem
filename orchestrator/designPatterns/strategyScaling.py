from abc import ABC, abstractmethod
import random
from orchestratorExceptions import *
from observer import Observer

class ScalingContext():
	def __init__(self, strategyName, containers):
		self.strategies = {"request": RequestScaling(containers)}
		self.setStrategy(strategyName)

	def setStrategy(self, strategyName):
		if strategyName in self.strategies.keys():
			self.strategy = self.strategies[strategyName]
		else:
			raise InvalidScalingChoice

	def scale(self):
		self.strategy.scale()

class StrategyScaling(ABC):
	@abstractmethod
	def scale(self):
		pass

class RequestScaling(StrategyScaling):
	def __init__(self, containers):
		self._containers = containers
	def scale(self):
		try:
			self._currentContainer = next(self._iterator)
			return self._currentContainer
		except:
			self._iterator = iter(self._containers)
			self._currentContainer = next(self._iterator)
			return self._currentContainer
