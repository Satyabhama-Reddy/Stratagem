from abc import ABC, abstractmethod
import random

class StrategyScaling(ABC):
	@abstractmethod
	def choose(self):
		pass

class RequestScaling(StrategyScaling):
	def __init__(self, containers):
		self._containers = containers
		self._iterator = iter(containers)
		self._currentContainer = None
	def choose(self):
		try:
			self._currentContainer = next(self._iterator)
			return self._currentContainer
		except:
			self._iterator = iter(self._containers)
			self._currentContainer = next(self._iterator)
			return self._currentContainer
