import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import multiprocessing

class Data:

    def __init__(self, filename):
        self.raw_data = pd.read_pickle(filename)

        #self.raw_data["min_sched_interval"] = self.raw_data["min_sched_interval"].apply(lambda x: str(x))
        #print(self.raw_data["min_sched_interval"].map(lambda x: "x" + str(x)))
        #print(self.raw_data["min_sched_interval"].unique())
        mins = self.raw_data.groupby(["graph_id", "cluster_name", "bandwidth", "netmodel"])["time"].transform(pd.Series.min)
        self.raw_data["score"] = self.raw_data["time"] / mins

    def prepare(self,
                cluster_name=None,
                exclude_single=False,
                netmodel="minmax",
                min_sched_interval=0.1):
        rd = self.raw_data

        if netmodel:
            f = rd["netmodel"] == netmodel
        else:
            f = rd["netmodel"].isin(["simple", "minmax"])

        if min_sched_interval is not None:
            f &= rd["min_sched_interval"] == min_sched_interval
        else:
            f &= rd["min_sched_interval"].isin([0.0, 0.1, 0.4, 1.6, 6.4])

        f &= rd["imode"] == "exact"
        #f &= rd["scheduler_name"].isin(["blevel", "random-gt", "genetic"])
        if cluster_name:
            f &= rd["cluster_name"] == cluster_name
        if cluster_name:
            f &= rd["scheduler_name"] != "single"
        return pd.DataFrame(rd[f])


def splot(data, col, row, x, y, hue, style=None, sharex=False, sharey=True, ylim=None):
    """
    g = sns.FacetGrid(data, col=col, row=row, sharey=sharey, sharex=sharex, margin_titles=True)
    if ylim is not None:
        g.set(ylim=ylim)

    def draw(**kw):
        data = kw["data"]
        #data["min_sched_interval"] = data["min_sched_interval"].astype(str)
        #data["bandwidth"] = data["bandwidth"]
        #ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, style=style)
        #ax.set(xscale="log")
        #hue_order = sorted(data[hue].unique())
        hue_order = None
        #if hue:
        #    hue_order = sorted(data[hue].unique())
        ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, hue_order=hue_order, style=style)
        ax.set(xscale="log")
        ax = sns.lineplot(data=data, x=x, y=y, hue=hue, hue_order=hue_order, style=style, ci=None)
        ax.set(xscale="log")
    g.map_dataframe(draw).add_legend()
    for ax in g.axes.flat:
        plt.setp(ax.texts, text="")
    g.set_titles(row_template="{row_name}", col_template="{col_name}", size = 2)
    """
    rows = sorted(data[col].unique())
    cols = sorted(data[row].unique())
    idata = pd.DataFrame(data, index=[col, row])
    idata.set_index([col, row], inplace=True)
    fig, axes = plt.subplots(nrows=len(rows), ncols=len(cols), figsize=(len(rows), len(cols)))
    for i, c in enumerate(cols):
        for j, r in enumerate(rows):
            gdata = idata.loc[(c, r)]
            print(gdata)




def process(name):
    print("processing " + name)
    data = Data("../results/" + name + ".zip")

    # ----- Schedulers -----
    #dataset = data.prepare()

    #splot(dataset, "cluster_name", "graph_name", x="bandwidth", y="score", hue="scheduler_name", sharey=False, ylim=(1, 3))
    #plt.savefig("outputs/" + name + "-schedulers-score.png")

    #splot(dataset, "cluster_name", "graph_name", x="bandwidth", y="time", hue="scheduler_name", style=None, sharey=False)
    #plt.savefig("outputs/" + name + "-schedulers-time.png")

    # ----- Netmodel -----
    dataset = data.prepare(cluster_name="16x4", netmodel=None, exclude_single=True)

    #splot(dataset, "graph_name", "scheduler_name", x="bandwidth", y="time", hue="netmodel", sharey=False)
    #plt.savefig("outputs/" + name + "-16x4-netmodel-time.png")

    #groups = dataset.groupby(["graph_name", "graph_id", "cluster_name", "bandwidth", "scheduler_name", "netmodel"])
    #means = groups["time"].mean().unstack().dropna()
    #score = pd.DataFrame((means["minmax"] / means["simple"]), columns=["score"]).reset_index()
    #splot(score, "graph_name", "scheduler_name", x="bandwidth", y="score", hue=None, sharey=False)
    #plt.savefig("outputs/" + name + "-16x4-netmodel-score.png")

    # ----- MinSchedTime
    dataset = data.prepare(cluster_name="16x4", min_sched_interval=None, exclude_single=True)
    splot(dataset, "graph_name", "scheduler_name", x="bandwidth", y="time", hue="min_sched_interval", style="min_sched_interval", sharey=False)
    plt.savefig("outputs/" + name + "-16x4-schedtime-time.png")

    #print(dataset)

    return name


if not os.path.isdir("outputs"):
    os.mkdir("outputs")

"""
names = ["pegasus", "elementary", "irw"]

pool = multiprocessing.Pool()
for name in pool.imap(process, names):
    print("finished", name)
"""
#process("pegasus")
#process("rg")
#process("elementary")
process("irw")



#plt.show()