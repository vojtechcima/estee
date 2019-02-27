from estee.common import TaskGraph
from estee.schedulers import BlevelGtScheduler
from estee.worker import Worker
from estee.simulator import Simulator
from estee.communication import MaxMinFlowNetModel

# Create task graph containing 3 tasks:
# t0 -> t1
#  L -> t2
tg = TaskGraph()
t0 = tg.new_task(duration=1, cpus=1, outputs=(1,))
t1 = tg.new_task(duration=1, cpus=1)
t1.add_input(t0)
t2 = tg.new_task(duration=1, cpus=1)
t2.add_input(t0)

# Create scheduler
scheduler = BlevelGtScheduler()

# Define cluster with 2 workers (1 CPU each)
workers = [Worker(cpus=1) for _ in range(2)]

# Define MaxMinFlow network model (100MB/s)
netmodel = MaxMinFlowNetModel(bandwidth=100)

# Create simulator
simulator = Simulator(tg, workers, scheduler, netmodel)

# Run simulation 
result = simulator.run()

# Print simulation time
print("Task graph execution makespan = {}".format(result))