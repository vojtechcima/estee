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

    def prepare(self, cluster_name=None, exclude_single=False, netmodel="minmax"):
        rd = self.raw_data

        f = rd["imode"] == "exact"
        #f &= rd["scheduler_name"].isin(["blevel", "random-gt", "genetic"])
        if netmodel:
            f &= rd["netmodel"] == netmodel
        else:
            f &= rd["netmodel"].isin(["simple", "minmax"])
        if cluster_name:
            f &= rd["cluster_name"] == cluster_name
        if cluster_name:
            f &= rd["scheduler_name"] != "single"
        f &= rd["min_sched_interval"] == 0.1
        return pd.DataFrame(rd[f])


def splot(data, col, row, x, y, hue, style=None, sharex=False, sharey=True, ylim=None):
    g = sns.FacetGrid(data, col=col, row=row, sharey=sharey, sharex=sharex, margin_titles=True)
    if ylim is not None:
        g.set(ylim=ylim)
    def draw(**kw):
        data = kw["data"]
        #data["min_sched_interval"] = data["min_sched_interval"].astype(str)
        #data["bandwidth"] = data["bandwidth"]
        #ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, style=style)
        #ax.set(xscale="log")
        hue_order = sorted(data[hue].unique())
        ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, hue_order=hue_order, style=style, size=0.8)
        ax.set(xscale="log")
        ax = sns.lineplot(data=data, x=x, y=y, hue=hue, hue_order=hue_order, style=style, legend="full", ci=None)
        ax.set(xscale="log")
    g.map_dataframe(draw).add_legend()



def process(name):
    print("processing " + name)
    data = Data("../results/" + name + ".zip")

    # ----- Schedulers -----
    dataset = data.prepare()

    splot(dataset, "graph_name", "cluster_name", x="bandwidth", y="score", hue="scheduler_name", sharey=False, ylim=(1, 3))
    plt.savefig(name + "-schedulers-score.png")

    splot(dataset, "graph_name", "cluster_name", x="bandwidth", y="time", hue="scheduler_name", style=None, sharey=False)
    plt.savefig(name + "-schedulers-time.png")

    # ----- Netmodel -----
    dataset = data.prepare(cluster_name="16x4", netmodel=None, exclude_single=True)

    splot(dataset, "graph_name", "scheduler_name", x="bandwidth", y="time", hue="netmodel", sharey=False)
    plt.savefig(name + "-netmodel-score.png")

process("pegasus")
#process("rg")
process("elementary")
process("irw")



#plt.show()