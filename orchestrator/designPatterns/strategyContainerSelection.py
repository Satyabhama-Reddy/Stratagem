from abc import ABC, abstractmethod

class StrategyContainerSelection(ABC):
	@abstractmethod
	def choose(self):
		pass

class RoundRobinSelection(ABC):
	def __init__(self, containers):
		self
	def choose(self):