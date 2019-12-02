from objectPool import ContainerPool
from strategyContainerSelection import RoundRobinSelection, MaxCPUSelection, RandomSelection

containers = ContainerPool(2, 4)
rr = RandomSelection(containers)

for a in range(10):
	print(rr.choose().port)
	if a==5:
		containers.acquire()