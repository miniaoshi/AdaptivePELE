import socket
machine = socket.gethostname()
import matplotlib
if machine == "bsccv03":
   matplotlib.use('wxagg')
import matplotlib.pyplot as plt
import numpy as np
import os
import collections
import argparse


def printHelp():
    """
        Create command line interface

        :returns: str -- Output filename ( if specified )
    """
    desc = "Program that prints the number of clusters throughout an adaptive sampling simulation. "\
            "It must be run in the root folder. "
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-filename", type=str, default="", help="Output filename")
    args = parser.parse_args()
    return args.filename


def getClusteringSummaryContent(summaryFile):
    """
        Get the contents of clustering summary file

        :param summaryFile: Clustering summary file
        :type summaryFile: str

        :returns: list -- List with the contents of the clustering summary file
    """
    if os.path.isfile(summaryFile):
        summaryContent = np.genfromtxt(summaryFile)
        if summaryContent.ndim > 1:
            return summaryContent
        elif summaryContent.ndim == 1:
            # file has only one line
            return np.array([summaryContent])
        else:
            # file existed but was empty
            return []
    else:
        return []


def getTotalNumberOfClustersPerEpoch(templetizedClusteringSummaryFile, folder):
    """
        Get the number of clusters in each epoch

        :param templetizedClusteringSummaryFile: Template name of the
            clustering summary file
        :type templetizedClusteringSummaryFile: str
        :param folder: Folder where the simulation data is stored
        :type folder: str

        :returns: list -- List with the number of cluster in each simulation
            epoch
    """
    allFolders = os.listdir(folder)
    numberOfEpochs = len([epoch for epoch in allFolders if epoch.isdigit() and os.path.isfile(templetizedClusteringSummaryFile%int(epoch))])

    totalNumberOfClustersPerEpoch = []
    for epoch in range(numberOfEpochs):
        clusteringSummary = getClusteringSummaryContent(templetizedClusteringSummaryFile % epoch)

        if clusteringSummary != []:
            totalNumberOfClustersPerEpoch.append(len(clusteringSummary))

    return totalNumberOfClustersPerEpoch

def findDifferentClustersInEpoch(column, summaryFile):
    """
        Get the distribution of values of a certain column in the clustering
            summary

        :param column: Column of interest
        :type column: int
        :param summaryFile: Clustering summary file
        :type summaryFile: str
        :returns: dict -- Dictionary with the set of different elements in
            column and the number of elements in this epoch
    """
    clusteringSummary = getClusteringSummaryContent(summaryFile)

    epochDictionary = {}
    if clusteringSummary != []:
        for line in clusteringSummary:
            value = line[column]
            if not value in epochDictionary:
                epochDictionary[value] = len(np.argwhere(clusteringSummary[:,column] == value))
    return epochDictionary

def findDifferentClustersForAllEpochs(column, templetizedClusteringSummaryFile, numberOfEpochs):
    """
        Get the distribution of values of a certain column in the clustering
            summary for each epoch

        :param column: Column of interest
        :type column: int
        :param templetizedClusteringSummaryFile: Template name of the
            clustering summary file
        :type templetizedClusteringSummaryFile: str
        :param numberOfEpochs: Total number of epochs in the simulation
        :type numberOfEpochs: int

        :returns: list -- List with dictionaries for all epochs. The dictionary
            has the set of different values (according to column) and their
            number
    """
    clustersPerEpoch = []
    for epoch in range(numberOfEpochs):
        summaryFile = templetizedClusteringSummaryFile%epoch
        epochDictionary = findDifferentClustersInEpoch(column, summaryFile)

        clustersPerEpoch.append(epochDictionary)
    return clustersPerEpoch

def getAllDifferentValues(clustersPerEpoch):
    """
        Get all the different values ocurring during a simulation

        :param clustersPerEpoch: List with dictionaries for all epochs. The dictionary
            has the set of different values (according to column) and their
            number
        :type clustersPerEpoch: list

        :returns: set -- Set containing all values ocurring during a simulation
    """
    allValues = set()
    for epochSummary in clustersPerEpoch:
        for value, numClusters in epochSummary.iteritems():
            allValues.update([value])
    return allValues

def buildClustersPerValue(clustersPerEpoch, numberOfEpochs):
    """
        Get the number of clusters that have each value

        :param clustersPerEpoch: List with dictionaries for all epochs. The dictionary
            has the set of different values (according to column) and their
            number
        :type clustersPerEpoch: list
        :param numberOfEpochs: Total number of epochs in the simulation
        :type numberOfEpochs: int

        :returns: dict -- Dictionary with the number of clusters that have each
            value
    """
    clustersPerValue = collections.defaultdict(list)

    allValues = getAllDifferentValues(clustersPerEpoch)

    for epochSummary in clustersPerEpoch:
        foundValues = set()
        for value, numClusters in epochSummary.iteritems():
            clustersPerValue[value].append(numClusters)
            foundValues.update([value])

        for value in allValues - foundValues:
            clustersPerValue[value].append(0)

    return clustersPerValue

def getNumberOfClustersPerEpochForGivenColumn(column, templetizedClusteringSummaryFile, folder):
    """
        Get the number of clusters that have each value at each epoch

        :param column: Column of interest
        :type column: int
        :param templetizedClusteringSummaryFile: Template name of the
            clustering summary file
        :type templetizedClusteringSummaryFile: str
        :param folder: Folder where the simulation data is stored
        :type folder: str

        :returns: dict -- Dictionary with the number of clusters that have each
            value
    """
    allFolders = os.listdir(folder)
    numberOfEpochs = len([epoch for epoch in allFolders if epoch.isdigit() and os.path.isfile(templetizedClusteringSummaryFile%int(epoch))])

    clustersPerEpoch = findDifferentClustersForAllEpochs(column, templetizedClusteringSummaryFile, numberOfEpochs)

    return buildClustersPerValue(clustersPerEpoch, numberOfEpochs)


def plotClustersPerValue(clustersPerValue):
    """
        Plot the number of clusters that have a certain value

        :param clustersPerValue: Dictionary with the number of clusters that have each
            value
        :type clustersPerValue: dict
    """
    values = clustersPerValue.keys()
    sortedValues = np.sort(values)
    for value in sortedValues:
        plt.plot(clustersPerValue[value], label=str(value))


def plotContactsHistogram(folder, templetizedClusteringSummaryFile):
    """
        Plot the histogram of the number of contacts

        :param folder: Folder where the simulation data is stored
        :type folder: str
        :param templetizedClusteringSummaryFile: Template name of the
            clustering summary file
        :type templetizedClusteringSummaryFile: str
    """
    allFolders = os.listdir(folder)
    lastEpoch = len([epoch for epoch in allFolders if epoch.isdigit() and os.path.isfile(templetizedClusteringSummaryFile%int(epoch))]) - 1
    lastSummary = templetizedClusteringSummaryFile%lastEpoch
    contactsColumn = 3
    allContacts = np.loadtxt(lastSummary, usecols=(contactsColumn,), ndmin=1)
    plt.hist(allContacts)

def main():
    """
        Plot a summary of the clustering for a simulation:
            1) Number of clusters for each threshold value at each epoch
            2) Number of clusters for each density value at each epoch
            3) Histogram of the number of contacts
    """
    filename = printHelp()

    print "FILENAME", filename

    #Params
    clusteringFileDensityColumn = 5
    clusteringFileThresholdColumn = 4
    clusteringFolder = "clustering"
    summaryFile = "summary.txt"
    folder = "."
    # end params

    clusteringSummaryFile = os.path.join(clusteringFolder, summaryFile)
    templetizedClusteringSummaryFile = os.path.join("%d", clusteringSummaryFile)


    totalNumberOfClustersPerEpoch = getTotalNumberOfClustersPerEpoch(templetizedClusteringSummaryFile, folder)
    clustersPerDensityValue = getNumberOfClustersPerEpochForGivenColumn(clusteringFileDensityColumn, templetizedClusteringSummaryFile, folder)
    clustersPerThresholdValue = getNumberOfClustersPerEpochForGivenColumn(clusteringFileThresholdColumn, templetizedClusteringSummaryFile, folder)

    plt.figure(1)
    plt.plot(totalNumberOfClustersPerEpoch, label="All clusters")
    if filename != "":
        plt.savefig("%s_total.png" % filename)

    plotClustersPerValue(clustersPerDensityValue)
    plt.legend(loc=2)
    if filename != "":
        plt.savefig("%s_density.png" % filename)

    plt.figure(2)
    plt.plot(totalNumberOfClustersPerEpoch, label="All clusters")
    plotClustersPerValue(clustersPerThresholdValue)
    plt.legend(loc=2)
    if filename != "":
        plt.savefig("%s_threshold.png" % filename)

    plt.figure(3)
    plotContactsHistogram(folder, templetizedClusteringSummaryFile)
    if filename != "":
        plt.savefig("%s_hist.png" % filename)

    plt.show()

if __name__ == "__main__":
    main()