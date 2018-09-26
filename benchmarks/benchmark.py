
from schedtk.taskgraph import TaskGraph
from schedtk import Worker, Simulator
from schedtk.connectors import SimpleConnector
from schedtk.generators import random_levels
from schedtk.schedulers import RandomAssignScheduler, BlevelGtScheduler, RandomGtScheduler

import random
import numpy as np
import pandas as pd


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
    data = np.array(
        [run_single_instance(task_graph, n_workers, scheduler_class())
            for _ in range(count)])
    average = np.average(data)
    std = data.std()
    minimum = data.min()
    return (minimum, average, std)


def main():
    n_workers = 3

    schedulers = [
        ("srandom", RandomAssignScheduler, 20),
        ("qrandom", RandomGtScheduler, 20),
        ("blevel1", lambda: BlevelGtScheduler(False), 1),
        ("blevel2", lambda: BlevelGtScheduler(True), 1),
    ]

    graphs = [make_graph() for _ in range(5)]

    columns = ["task_graph"]
    for name, _, _ in schedulers:
        columns.append(name + "_avg")
        columns.append(name + "_std")
    columns.append("min")

    results = []
    for graph in graphs:
        data = [graph]
        mins = []
        for name, scheduler, count, in schedulers:
            minimum, average, std = benchmark_scheduler(graph, scheduler, n_workers, count)
            mins.append(minimum)
            data.append(average)
            data.append(std)
        data.append(min(mins))
        results.append(data)

    data = pd.DataFrame(results, columns=columns)

    avg_names = [name + "_avg" for name, _, _ in schedulers]
    for n in avg_names:
        r = data[n] / data["min"]
        print(n, r.mean())



if __name__ == "__main__":
    main()