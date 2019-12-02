from abc import ABC, abstractmethod
import random
from orchestratorExceptions import *

class ContainerSelectionContext():
	def __init__(self, strategyName, containers):
		self.strategies = {"round robin": RoundRobinSelection(containers), "random": RandomSelection(containers), "cpu usage": MaxCPUSelection(containers)}
		self.setStrategy(strategyName)

	def setStrategy(self, strategyName):
		if strategyName in self.strategies.keys():
			self.strategy = self.strategies[strategyName]
		else:
			raise InvalidContainerSelectionChoice

	def choice(self):
		self.strategy.choose()

class StrategyContainerSelection(ABC):
	@abstractmethod
	def choose(self):
		pass

class RoundRobinSelection(StrategyContainerSelection):
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

class MaxCPUSelection(StrategyContainerSelection):
	def __init__(self, containers):
		self._containers = containers
	def choose(self):
		maxTotalUsage = -1
		bestContainer = None
		for container in self._containers:
			if maxTotalUsage==-1 or container.cpuUsage<maxTotalUsage:
				bestContainer = container
				maxTotalUsage = container.cpuUsage
		return bestContainer


class RandomSelection(StrategyContainerSelection):
	def __init__(self, containers):
		self._containers = containers
	def choose(self):
		return self._containers[random.randint(0, len(self._containers)-1)]