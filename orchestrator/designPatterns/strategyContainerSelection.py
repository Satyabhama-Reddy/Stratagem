from abc import ABC, abstractmethod
import random
from orchestratorExceptions import *
from observer import Observable

class ContainerSelectionContext():
	def __init__(self, strategyName, containers):
		self.strategies = {"round robin": RoundRobinSelection(containers), "random": RandomSelection(containers), "cpu usage": MaxCPUSelection(containers)}
		self.setStrategy(strategyName)

	def setStrategy(self, strategyName):
		if strategyName in self.strategies.keys():
			self.strategy = self.strategies[strategyName]
		else:
			raise InvalidContainerSelectionChoice

	def choose(self):
		return self.strategy.choose()

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
		except:
			self._iterator = iter(self._containers)
			self._currentContainer = next(self._iterator)
		finally:
			if self._currentContainer.requestCount!=0:
				return self.choose()
			return self._currentContainer


class MaxCPUSelection(StrategyContainerSelection):
	def __init__(self, containers):
		self._containers = containers
	def choose(self):
		maxTotalUsage = -1
		bestContainer = None
		while maxTotalUsage==-1:
			for container in self._containers:
				print(container.port, container.cpuUsage)
				if maxTotalUsage==-1 or container.cpuUsage<maxTotalUsage:
					bestContainer = container
					maxTotalUsage = container.cpuUsage
		return bestContainer


class RandomSelection(StrategyContainerSelection):
	def __init__(self, containers):
		self._containers = containers
	def choose(self):
		return self._containers[random.randint(0, len(self._containers)-1)]