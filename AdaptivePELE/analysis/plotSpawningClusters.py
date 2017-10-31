import socket
machine = socket.gethostname()
import matplotlib
if machine == "bsccv03":
   matplotlib.use('wxagg')
elif 'login' in machine:
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import numpy as np
import os
import argparse

def printHelp():
    """
        Create command line interface

        :returns: str -- Output filename ( if specified )
    """
    desc = "Program that prints the number of clusters of each threshold that"\
           "have been selected by the spwaning throughout an adaptive sampling simulation. "\
           "It must be run in the root folder. "
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-filename", type=str, default="", help="Output filename")
    args = parser.parse_args()
    return args.filename

def main():
    filename = printHelp()
    print "FILENAME", filename
    templateSummary = "%d/clustering/summary.txt"
    allFolders = os.listdir(".")
    numberOfEpochs = len([epoch for epoch in allFolders if epoch.isdigit() and
        os.path.isfile(templateSummary % int(epoch))])

    clustering = np.loadtxt(templateSummary % (numberOfEpochs-1))
    clustersThres = list(set(clustering[:,4]))
    clustersThres.sort(reverse=True)
    spawningPerThres = np.zeros((numberOfEpochs, len(clustersThres)))
    for i in xrange(numberOfEpochs):
        clustering = np.loadtxt(templateSummary % i)
        for j, threshold in enumerate(clustersThres):
            spawningPerThres[i, j] = clustering[clustering[:,4]==threshold, 2].sum()
    plt.plot(spawningPerThres)
    plt.legend(labels=map(lambda x: "Cluster size %d" % x, clustersThres),
               loc="best")
    plt.xlabel("Epoch")
    plt.ylabel("Number of spawned processors")
    if filename != "":
        plt.savefig("%s_spawning.png" % filename)
    plt.show()

if __name__ == "__main__":
    main()