import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os


class Data:

    def __init__(self, filename):
        self.raw_data = pd.read_pickle(filename)

        mins = self.raw_data.groupby(["graph_id", "cluster_name", "bandwidth", "netmodel"])["time"].transform(pd.Series.min)
        self.raw_data["score"] = self.raw_data["time"] / mins

    def prepare(self):
        rd = self.raw_data

        f = rd["imode"] == "exact"
        f &= rd["netmodel"] == "minmax"
        #f &= rd["cluster_name"] == "16x4"
        f &= rd["min_sched_interval"] == 0.1
        return pd.DataFrame(rd[f])


def splot(data, col, row, x, y, hue, style=None, sharex=False, sharey=True, ylim=None):
    g = sns.FacetGrid(data, col=col, row=row, sharey=sharey, sharex=sharex, margin_titles=True)
    g.set_titles()
    if ylim is not None:
        g.set(ylim=ylim)
    def draw(**kw):
        data = kw["data"]
        #data["min_sched_interval"] = data["min_sched_interval"].astype(str)
        #data["bandwidth"] = data["bandwidth"]
        #ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, style=style)
        #ax.set(xscale="log")
        ax = sns.lineplot(data=data, x=x, y=y, hue=hue, style=style, legend="full")
        ax.set(xscale="log")
    g.map_dataframe(draw).add_legend()



data = Data("../results/irw.zip")
dataset = data.prepare()

splot(dataset, "graph_name", "cluster_name", x="bandwidth", y="score", hue="scheduler_name", sharey=False, ylim=(0, 4))
plt.savefig("score.png")

splot(dataset, "graph_name", "cluster_name", x="bandwidth", y="time", hue="scheduler_name", sharey=False)
plt.savefig("time.png")


#plt.show()