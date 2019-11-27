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