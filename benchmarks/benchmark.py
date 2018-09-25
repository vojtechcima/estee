
from schedtk.taskgraph import TaskGraph
from schedtk import Worker, Simulator
from schedtk.connectors import SimpleConnector
from schedtk.generators import random_levels
from schedtk.schedulers import RandomAssignScheduler

import random
import numpy as np


def run_single_instance(task_graph, n_workers, scheduler):
    workers = [Worker() for _ in range(n_workers)]
    connector = SimpleConnector()
    simulator = Simulator(task_graph, workers, scheduler, connector)
    return simulator.run()


def make_graph():
    def make_node():
        return graph.new_task(None, duration=random.random(), size=random.random())

    graph = TaskGraph()
    random_levels(
        [(3, 10), (3, 20), (3, 20), (3, 10)],
        [0, (1, 5), (2, 6), (1, 5)],
        make_node)
    return graph


def benchmark_scheduler(task_graph, scheduler_class, n_workers, count):
    return np.array(
            [run_single_instance(task_graph, n_workers, scheduler_class())
            for _ in range(count)])


def main():
    n_workers = 3

    graphs = [make_graph() for _ in range(1)]

    for graph in graphs:
        task_graph = make_graph()
        results = benchmark_scheduler(task_graph, RandomAssignScheduler, n_workers, 100)

        average = np.average(results)
        minimum = results.min()
        print(average, minimum, average / minimum)


if __name__ == "__main__":
    main()