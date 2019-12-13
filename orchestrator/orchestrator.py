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
# from flask_restful import Resource, Api
from queue import PriorityQueue
import threading
import docker 
import random

import signal
import sys



client = docker.from_env()


class Orchestrator(Observer):
	def __init__(self,image,containerPort,port=5000, minContainers=2, maxContainers=4, containerSelectionChoice="round robin", scalingChoice={"strategy":"no scaling"}):
		try:
			if minContainers<=0 or type(minContainers)!=int:
				raise InvalidMinimumContainers
			if maxContainers<minContainers or type(maxContainers)!=int:
				raise InvalidMaximumContainers

			self._containerPool = ContainerPool(minContainers, maxContainers,image,containerPort)
			self._containerSelectionStrategy = ContainerSelectionContext(containerSelectionChoice, self._containerPool)
			self._containerScalingStrategy = ScalingContext(scalingChoice, self._containerPool)
			self._containerPool.numberContainers.subscribe(self)
			self.requestsQueue = PriorityQueue()
			signal.signal(signal.SIGINT, self.signal_handler)
			self.app = Flask(__name__)

			@self.app.route('/stratagem/containerSelection/<strategy>', methods=["POST"])
			def setContainerSelection(strategy):
				if request.remote_addr=="127.0.0.1":
					try:
						self._containerSelectionStrategy.setStrategy(strategy)
						print("Strategy", strategy, "set")
					except:
						print("Strategy invalid")
				else:
					print("Only localhost can change strategy")

				return ""

			@self.app.route('/stratagem/scaling', methods=["POST"])
			def setScaling():
				if request.remote_addr=="127.0.0.1":
					try:
						strategy=dict(request.get_json())
						self._containerScalingStrategy.setStrategy(strategy)
						print("Strategy", strategy, "set")
					except Exception as e:
						print("Strategy invalid",e)
				else:
					print("Only localhost can change strategy")

				return ""

			@self.app.route('/<path:path>',methods=['GET','POST','DELETE'])
			def proxy(*args, **kwargs):
				activeRequest = request

				selectedContainer = self._containerSelectionStrategy.choose()
				self._containerScalingStrategy.increment()
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
			try:
				self.app.run(threaded=True,port=port, host="0.0.0.0")
			except KeyboardInterrupt:
				print("exiting")

		except InvalidMinimumContainers:
			print("InvalidMinimumContainers: minContainers must be an integer value greater than 0 and lesser than or equal to maxContainers")
		except InvalidMaximumContainers:
			print("InvalidMaximumContainers: maxContainers must be an integer value greater than 0 and greater than or equal to minContainers")
		except InvalidContainerSelectionChoice:
			print("InvalidContainerSelectionChoice: containerSelectionChoice must be in \"round robin\", \"random\", \"cpu usage\"")
		except InvalidScalingChoice:
			print("InvalidScalingChoice: ScalingChoice")

	def update(self, arg):
		print("Number of Containers : ", arg)

	def destructor(self):
		# print("here")
		self._containerPool.destructor()

	def signal_handler(self, sig, frame):
		print('\nStopping Containers..')
		self.destructor()
		
		sys.exit(0)
		