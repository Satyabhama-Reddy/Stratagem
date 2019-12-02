import os
import sys
sys.path.insert(1, os.getcwd()+"/designPatterns")

from objectPool import ContainerPool
from strategyContainerSelection import ContainerSelectionContext
from strategyScaling import ScalingContext
from observer import Observer
from orchestratorExceptions import *
from flask import Flask, jsonify, request, Response
import requests
from flask_restful import Resource, Api
from queue import PriorityQueue
import threading
import docker 
import random
client = docker.from_env()

class Orchestrator(Observer):
	def __init__(self,image,port, minContainers=2, maxContainers=4, containerSelectionChoice="round robin", scalingChoice={"strategy":"no scaling"}):
		try:
			if minContainers<=0 or type(minContainers)!=int:
				raise InvalidMinimumContainers
			if maxContainers<minContainers or type(maxContainers)!=int:
				raise InvalidMaximumContainers

			self._containerPool = ContainerPool(minContainers, maxContainers,image,port)
			self._containerSelectionStrategy = ContainerSelectionContext(containerSelectionChoice, self._containerPool)
			# self._containerScalingStrategy = ScalingContext(scalingChoice, self._containerPool)
			self._containerPool.numberContainers.subscribe(self)

			self.requestsQueue = PriorityQueue()
			self.app = Flask(__name__)

			@self.app.route('/stratagem/containerSelection/<strategy>', methods=["GET"])
			def setContainerSelection(strategy):
				try:
					self._containerSelectionStrategy.setStrategy(strategy)
					print("Strategy", strategy, "set")
				except:
					print("Strategy invalid")

				return ""

			@self.app.route('/stratagem/scaling', methods=["POST"])
			def setScaling():
				try:
					self._containerScalingStrategy.setStrategy(dict(request.get_json()))
					print("Strategy", strategy, "set")
				except:
					print("Strategy invalid")

				return ""

			@self.app.route('/<path:path>',methods=['GET','POST','DELETE'])
			def proxy(*args, **kwargs):
				activeRequest = request

				selectedContainer = self._containerSelectionStrategy.choose()
				selectedContainer.requestCount+=1
				resp = requests.request(
					method=activeRequest.method,
					url=activeRequest.url.replace(activeRequest.host_url, 'http://127.0.0.1:'+str(selectedContainer.port)+'/'),
					headers={key: value for (key, value) in activeRequest.headers if key != 'Host'},
					data=activeRequest.get_data(),
					cookies=activeRequest.cookies,
					allow_redirects=False)
				selectedContainer.requestCount-=1

				excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
				headers = [(name, value) for (name, value) in resp.raw.headers.items()
						   if name.lower() not in excluded_headers]
				print("Request handled by port:", str(selectedContainer.port))
				return Response(resp.content, resp.status_code, headers)

			self.app.run(threaded=True, host="0.0.0.0")

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

	def __del__(self):
		print("here")
		del self._containerPool

if __name__ == "__main__":
	orchestrator = Orchestrator("flaskexample/flaskexample",5000,2, 4,"cpu usage",{"strategy":"no scaling"})









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