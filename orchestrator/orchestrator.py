import os
import sys
sys.path.insert(1, os.getcwd()+"/designPatterns")

from objectPool import ContainerPool
from strategyContainerSelection import RoundRobinSelection, MaxCPUSelection, RandomSelection
from observer import Observer

class Error(Exception):
	pass

class InvalidMinimumContainers(Error):
	pass

class InvalidMaximumContainers(Error):
	pass

class InvalidContainerSelectionChoice(Error):
	pass

class InvalidScalingChoice(Error):
	pass


class Orchestrator(Observer):
	def __init__(self, minContainers=2, maxContainers=4, containerSelectionChoice="round robin", scalingChoice="normal"):
		try:
			if minContainers<=0 or type(minContainers)!=int:
				raise InvalidMinimumContainers
			if maxContainers<=minContainers or type(maxContainers)!=int:
				raise InvalidMaximumContainers
			if containerSelectionChoice not in ["round robin", "random", "cpu usage"]:
				raise InvalidContainerSelectionChoice
			if scalingChoice not in ["round robin", "random", "cpu usage"]:
				raise InvalidScalingChoice

			containerSelectionObjects = {"round robin": RoundRobinSelection(), "random": RandomSelection(), "cpu usage": MaxCPUSelection()}

			self._containerPool = objectPool(minContainers, maxContainers)
			# self._containerSelectionStrategy = containerSelectionObjects

		except InvalidMinimumContainers:
			print("InvalidMinimumContainers: minContainers must be an integer value greater than 0 and lesser than or equal to maxContainers")
		except InvalidMaximumContainers:
			print("InvalidMaximumContainers: maxContainers must be an integer value greater than 0 and greater than or equal to minContainers")
		except InvalidContainerSelectionChoice:
			print("InvalidContainerSelectionChoice: containerSelectionChoice must be in \"round robin\", \"random\", \"cpu usage\"")
		except InvalidScalingChoice:
			print("InvalidScalingChoice: containerSelectionChoice must be in \"round robin\", \"random\", \"cpu usage\"")

	def update(self, arg):
		print("Value is", arg)

orchestrator = Orchestrator(2, 4, "round robin", "random")

"""
class Orchestrator:
	def __init__(self, ...):
		- strategy load balancing
		- strategy scaling
		- container object pool
		- observable container count
		- initialize scaling thread


	def __del__(self):
		- delete containers

	def __run__(self):
		- run the orchestrator at some port

	@self.app.route('/', defaults={'path': ''},methods=['GET','POST','DELETE'])
	@self.app.route('/<path:path>',methods=['GET','POST','DELETE'])
	def proxy(self):
		- direct strategy related things to the respective functions
		- use strategy object to select th container







	container parmeters
	strategy

	container count -> Observable
	notify -> container count changes,

	Object Pool -> containers stored by id

	docker stats: https://docs.docker.com/engine/reference/commandline/stats/
	states are updated by a daemon thread.

	handlers for strategy changes:
		strategem/loadbalancing/<name>
		strategem/scaling/<name>

	Constructor():
		get docker image
		initialize minimum contaniner objects
		create container_count as observable


	make it a singleton
"""