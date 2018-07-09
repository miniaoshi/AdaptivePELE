from __future__ import absolute_import, division, print_function, unicode_literals
import time
import os
import json
import subprocess
import shutil
import string
import sys
import numpy as np
import ast
import glob
import itertools
import multiprocessing as mp
from builtins import range
from AdaptivePELE.constants import constants, blockNames
from AdaptivePELE.simulation import simulationTypes
from AdaptivePELE.atomset import atomset, RMSDCalculator
from AdaptivePELE.utilities import utilities
SKLEARN = True
OPENMM = True
try:
    from sklearn.cluster import KMeans
except ImportError:
    SKLEARN = False
try:
    basestring
except NameError:
    basestring = str
try:
    import simtk.openmm as mm
    import simtk.openmm.app as app
    import simtk.unit as unit
except ImportError:
    OPENMM = False


class SimulationParameters:
    def __init__(self):
        self.processors = 0
        self.executable = ""
        self.templetizedControlFile = ""
        self.dataFolder = ""
        self.documentsFolder = ""
        self.iterations = 0
        self.peleSteps = 0
        self.seed = 0
        self.exitCondition = None
        self.boxCenter = None
        self.boxRadius = 20
        self.modeMovingBox = None
        self.runEquilibration = False
        self.equilibrationLength = None
        self.destination = None
        self.origin = None
        self.equilibrationMode = ""
        self.SASAforBox = None
        self.columnSASA = None
        self.reportName = None
        self.trajectoryName = None
        self.srun = False
        self.numberEquilibrationStructures = 10
        # parameters needed for MD simulations and their defaults
        self.ligandCharge = 0
        self.nonBondedCutoff = 8
        self.Temperature = 300
        self.runningPlatform = "CPU"
        self.minimizationIterations = 2000
        self.reporterFreq = None
        self.energyReport = True
        self.productionLength = 0


class SimulationRunner:
    def __init__(self, parameters):
        self.parameters = parameters
        self.processorsToClusterMapping = []

    def runSimulation(self, epoch, outputPathConstants, initialStructuresAsString, topologies):
        pass

    def getWorkingProcessors(self):
        """
            Return the number of working processors, i.e. number of trajectories
        """
        return self.parameters.processors

    def hasExitCondition(self):
        """
            Check if an exit condition has been set

            :returns: bool -- True if an exit condition is set
        """
        return self.parameters.exitCondition is not None

    def checkSimulationInterrupted(self, epoch):
        """
            Check wether the simulation was interrupted before finishing

            :param epoch: Epoch number
            :type epoch: int

            :returns: bool -- True if the simulations where interrupted
        """
        # for Pele and Test simulation there is no proper way to check so return
        # False and rely on the clustering for such check
        return False

    def cleanCheckpointFiles(self, epoch):
        """
            Clean the restart files generated if the simulation was interrupted
            before finishing

            :param epoch: Epoch number
            :type epoch: int
        """
        # for Pele and Test simulation there is no proper way to restart, so
        # just pass
        pass

    def checkExitCondition(self, clustering, outputFolder):
        """
            Check if the exit condition has been met

            :param clustering: Clustering object
            :type clustering: :py:class:`.Clustering`

            :returns: bool -- True if the exit condition is met
        """
        if self.parameters.exitCondition.type == simulationTypes.EXITCONDITION_TYPE.METRICMULTIPLETRAJS:
            return self.parameters.exitCondition.checkExitCondition(outputFolder)
        else:
            return self.parameters.exitCondition.checkExitCondition(clustering)

    def makeWorkingControlFile(self, workingControlFilename, dictionary, inputTemplate=None):
        """
            Substitute the values in the templetized control file

            :param workingControlFilename: Name of the template control file
            :type workingControlFilename: str
            :param dictionary: Dictonary containing the parameters to substitute
                in the control file
            :param inputFileTemplate: Template control file
            :type inputFileTemplate: str
            :type dictionary: dict
        """
        if inputTemplate is None:
            with open(self.parameters.templetizedControlFile, "r") as inputFile:
                inputFileContent = inputFile.read()
        else:
            inputFileContent = inputTemplate

        inputFileTemplate = string.Template(inputFileContent)
        outputFileContent = inputFileTemplate.substitute(dictionary)
        with open(workingControlFilename, "w") as outputFile:
            outputFileContent = outputFileContent.replace("'", '"')
            outputFile.write(outputFileContent)

    def updateMappingProcessors(self, mapping):
        """
            Update the value of the processorsToClusterMapping, a list with the
            snapshot from which the trajectories will start in the next iteration

            :param mapping: List with the snapshot from which the trajectories
                will start in the next iteration
            :type mapping: list
        """
        self.processorsToClusterMapping = mapping[1:]+[mapping[0]]

    def writeMappingToDisk(self, epochDir):
        """
            Write the processorsToClusterMapping to disk

            :param epochDir: Name of the folder where to write the
                processorsToClusterMapping
            :type epochDir: str
        """
        if len(self.processorsToClusterMapping) == 0:
            return
        with open(epochDir+"/processorMapping.txt", "w") as f:
            f.write(':'.join(map(str, self.processorsToClusterMapping)))

    def readMappingFromDisk(self, epochDir):
        """
            Read the processorsToClusterMapping from disk

            :param epochDir: Name of the folder where to write the
                processorsToClusterMapping
            :type epochDir: str
        """
        try:
            with open(epochDir+"/processorMapping.txt") as f:
                self.processorsToClusterMapping = map(ast.literal_eval, f.read().rstrip().split(':'))
        except IOError:
            sys.stderr.write("WARNING: processorMapping.txt not found, you might not be able to recronstruct fine-grained pathways\n")

    def setZeroMapping(self):
        """
            Set the processorsToClusterMapping to zero
        """
        self.processorsToClusterMapping = [0 for _ in range(1, self.parameters.processors)]

    def createMultipleComplexesFilenames(self, numberOfSnapshots, tmpInitialStructuresTemplate, iteration, equilibration=False):
        """
            Creates the string to substitute the complexes in the PELE control file

            :param numberOfSnapshots: Number of complexes to write
            :type numberOfSnapshots: int
            :param tmpInitialStructuresTemplate: Template with the name of the initial strutctures
            :type tmpInitialStructuresTemplate: str
            :param iteration: Epoch number
            :type iteration: int
            :param equilibration: Flag to mark wether the complexes are part of an
                equilibration run
            :type equilibration: bool

            :returns: str -- jsonString to be substituted in PELE control file
        """
        pass

    def prepareControlFile(self, epoch, outputPathConstants, peleControlFileDictionary):
        """
            Substitute the parameters in the PELE control file specified with the
            provided in the control file

            :param epoch: Epoch number
            :type epoch: int
            :param outputPathConstants: Object that has as attributes constant related to the outputPath that will be used to create the working control file
            :type outputPathConstants: :py:class:`.OutputPathConstants`
            :param peleControlFileDictionary: Dictonary containing the values of the parameters to substitute in the control file
            :type peleControlFileDictionary: dict
        """
        outputDir = outputPathConstants.epochOutputPathTempletized % epoch
        peleControlFileDictionary["OUTPUT_PATH"] = outputDir
        peleControlFileDictionary["SEED"] = self.parameters.seed + epoch * self.parameters.processors
        if self.parameters.boxCenter is not None:
            peleControlFileDictionary["BOX_RADIUS"] = self.parameters.boxRadius
            peleControlFileDictionary["BOX_CENTER"] = self.parameters.boxCenter
        self.makeWorkingControlFile(outputPathConstants.tmpControlFilename % epoch, peleControlFileDictionary)


class PeleSimulation(SimulationRunner):
    def __init__(self, parameters):
        SimulationRunner.__init__(self, parameters)
        self.type = simulationTypes.SIMULATION_TYPE.PELE

    def createSymbolicLinks(self):
        """
            Create symbolic links to Data and Documents folder if they don't exist
        """
        if not os.path.islink("Data"):
            os.system("ln -s " + self.parameters.dataFolder + " Data")
        if not os.path.islink("Documents"):
            os.system("ln -s " + self.parameters.documentsFolder + " Documents")

    def getWorkingProcessors(self):
        """
            Return the number of working processors, i.e. number of trajectories
        """
        return self.parameters.processors-1

    def getNextIterationBox(self, clusteringObject, outputFolder, resname, topologies=None, epoch=None):
        """
            Select the box for the next epoch, currently selecting the COM of
            the cluster with max SASA

            :param clusteringObject: Clustering object
            :type clusteringObject: :py:class:`.Clustering`
            :param outputFolder: Folder to the trajectories
            :type outputFolder: str
            :param resname: Name of the ligand in the pdb
            :type resname: str
            :param topologies: Topology object containing the set of topologies needed for the simulation
            :type topologies: :py:class:`.Topology`
            :param epoch: Epoch of the trajectories to analyse
            :type epoch: int

            :returns str: -- string to be substitued in PELE control file
        """
        metrics = utilities.getMetricsFromReportsInEpoch(self.parameters.reportName, outputFolder, self.parameters.processors)
        if self.parameters.modeMovingBox.lower() == blockNames.SimulationParams.modeMovingBoxBinding:
            SASAcluster = np.argmin(metrics[:, self.parameters.columnSASA])
            if metrics[SASAcluster, self.parameters.columnSASA] < self.parameters.SASAforBox:
                self.parameters.SASAforBox = metrics[SASAcluster, self.parameters.columnSASA]
            else:
                return
        elif self.parameters.modeMovingBox.lower() == blockNames.SimulationParams.modeMovingBoxUnBinding:
            SASAcluster = np.argmax(metrics[:, self.parameters.columnSASA])
            if metrics[SASAcluster, self.parameters.columnSASA] > self.parameters.SASAforBox:
                self.parameters.SASAforBox = metrics[SASAcluster, self.parameters.columnSASA]
            else:
                return
        else:
            raise ValueError("%s should be either binding or unbinding, but %s is provided!!!" % (blockNames.SimulationParams.modeMovingBox, self.parameters.modeMovingBox))
        # If this lines are reached then a new extreme SASA value was
        # identified and we proceed to extract the corresponding center of mass
        trajNum = metrics[SASAcluster, -2]
        snapshotNum = metrics[SASAcluster, -1]
        snapshot = utilities.getSnapshots(os.path.join(outputFolder, self.parameters.trajectoryName % trajNum))[int(snapshotNum)]
        snapshotPDB = atomset.PDB()
        snapshotPDB.initialise(snapshot, resname=resname, topology=topologies.getTopology(epoch, trajNum))
        self.parameters.boxCenter = str(snapshotPDB.getCOM())
        return

    def selectInitialBoxCenter(self, initialStructuresAsString, resname):
        """
            Select the coordinates of the first box, currently as the center of
            mass of the first initial structure provided

            :param initialStructuresAsString: String containing the files of the initial structures
            :type initialStructuresAsString: str
            :param resname: Residue name of the ligand in the system pdb
            :type resname: str

            :returns str: -- string to be substitued in PELE control file
        """
        # This is a dictionary because it's prepared to be subtitued in the PELE
        # control files (i.e. JSON format)
        try:
            initialStructuresDict = json.loads(initialStructuresAsString.split(",")[0])
            initialStruct = str(initialStructuresDict['files'][0]['path'])
        except ValueError:
            # If a json valid string is not passed, interpret the input string
            # as a path to a file
            initialStruct = initialStructuresAsString

        # Note: this lines were not changed when adding support for xtc
        # trajectories because it was assumed that initial structures would
        # still be pdbs
        PDBinitial = atomset.PDB()
        PDBinitial.initialise(initialStruct, resname=resname)
        return repr(PDBinitial.getCOM())

    def runSimulation(self, epoch, outputPathConstants, initialStructuresAsString, topologies):
        """
        Run a short PELE simulation

        :param epoch: number of the epoch
        :param outputPathConstants: outputpathConstants class
        :param ControlFileDictionary: Dictionary with the values to substitute in the template
        :param topologies: topology class
        """

        print("Preparing Control File")
        ControlFileDictionary = {"COMPLEXES": initialStructuresAsString,
                                 "PELE_STEPS": self.parameters.peleSteps,
                                 "BOX_RADIUS": self.parameters.boxRadius}
        self.prepareControlFile(epoch, outputPathConstants, ControlFileDictionary)
        self.createSymbolicLinks()
        runningControlFile = outputPathConstants.tmpControlFilename % epoch
        if self.parameters.srun:
            toRun = ["srun", self.parameters.executable, runningControlFile]
        else:
            toRun = ["mpirun -np " + str(self.parameters.processors), self.parameters.executable, runningControlFile]
        toRun = " ".join(toRun)
        print(toRun)
        startTime = time.time()
        proc = subprocess.Popen(toRun, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        (out, err) = proc.communicate()
        print(out)
        if err:
            print(err)

        endTime = time.time()
        print("PELE took %.2f sec" % (endTime - startTime))

    def getEquilibrationControlFile(self, peleControlFileDict):
        """
            Filter unnecessary parameters and return a minimal PELE control
            file for equilibration runs

            :param peleControlFileDict: Dictionary with pele control file options
            :type peleControlFileDict: dict

            :returns: dict -- Dictionary with pele control file options
        """
        # Set small rotations and translations
        peleControlFileDict["commands"][0]["Perturbation"]["parameters"]["translationRange"] = 0.5
        peleControlFileDict["commands"][0]["Perturbation"]["parameters"]["rotationScalingFactor"] = 0.05
        # Remove dynamical changes in control file
        peleControlFileDict["commands"][0]["PeleTasks"][0].pop("exitConditions", None)
        peleControlFileDict["commands"][0]["PeleTasks"][0].pop("parametersChanges", None)
        # Set box_radius to 2
        peleControlFileDict["commands"][0]["Perturbation"]["Box"]["fixedCenter"] = "$BOX_CENTER"
        peleControlFileDict["commands"][0]["Perturbation"]["Box"]["radius"] = 2
        # Ensure random tags exists in metrics
        metricsBlock = peleControlFileDict["commands"][0]["PeleTasks"][0]["metrics"]
        nMetrics = len(metricsBlock)
        randomIndexes = sorted([i for i in range(nMetrics) if metricsBlock[i]['type'] == "random"])
        # Delete random numbers from metrics
        for index in randomIndexes[::-1]:
            del metricsBlock[index]
        nMetrics = len(metricsBlock)
        # Add new random number to metrics
        metricsBlock.extend([{'tag': 'rand', 'type': 'random'}])
        # Add equilibration dynamical changes
        changes = {
            "doThesechanges": {
                "Perturbation::parameters": {"rotationScalingFactor": 0.050}
            },
            "ifAnyIsTrue": ["rand >= .5"],
            "otherwise": {
                "Perturbation::parameters": {"rotationScalingFactor": 0.15}
            }
            }
        peleControlFileDict["commands"][0]["PeleTasks"][0]["parametersChanges"] = [changes]

        return peleControlFileDict

    def getMetricColumns(self, JSONdict):
        """
            Extract the column of a similarity distance (RMSD or distance) from the pele control file

            :param JSONdict: Dictionary containing a parsed PELE control file
            :type JSONdict: dict

            :returns: int -- Column index of the similarity metric
        """
        hasRMSD = False
        RMSDCol = None
        distanceCol = None
        hasDistance = False
        for i, metricBlock in enumerate(JSONdict["commands"][0]["PeleTasks"][0]['metrics']):
            if 'rmsd' in metricBlock['type'].lower():
                hasRMSD = True
                RMSDCol = i+4
            elif 'distance' in metricBlock['type'].lower():
                hasDistance = True
                distanceCol = i+4
        if hasRMSD:
            return RMSDCol
        elif hasDistance:
            return distanceCol
        else:
            return None

    def calculateEquilibrationLength(self):
        """
            Calculate the number of steps for the equilibration lenght accoding
            to the available processors
        """
        # Total steps is an approximate number of total steps to produce
        totalSteps = 1000
        # Take at least 5 steps
        stepsPerProc = max(int(totalSteps/float(self.parameters.processors)), 5)
        # but no more than 50
        return min(stepsPerProc, 50)

    def equilibrate(self, initialStructures, outputPathConstants, reportFilename, outputPath, resname, topologies=None):
        """
            Run short simulation to equilibrate the system. It will run one
            such simulation for every initial structure and select appropiate
            structures to start the simulation

            :param initialStructures: Name of the initial structures to copy
            :type initialStructures: list of str
            :param outputPathConstants: Contains outputPath-related constants
            :type outputPathConstants: :py:class:`.OutputPathConstants`
            :param reportBaseFilename: Name of the file that contains the metrics of the snapshots to cluster
            :type reportBaseFilename: str
            :param outputPath: Path where trajectories are found
            :type outputPath: str
            :param resname: Residue name of the ligand in the system pdb
            :type resname: str
            :param topologies: Topology object containing the set of topologies needed for the simulation
            :type topologies: :py:class:`.Topology`

            :returns: list --  List with initial structures
        """
        newInitialStructures = []
        newStructure = []
        if self.parameters.equilibrationLength is None:
            self.parameters.equilibrationLength = self.calculateEquilibrationLength()
        equilibrationPeleDict = {"PELE_STEPS": self.parameters.equilibrationLength, "SEED": self.parameters.seed}
        peleControlFileDict, templateNames = utilities.getPELEControlFileDict(self.parameters.templetizedControlFile)
        peleControlFileDict = self.getEquilibrationControlFile(peleControlFileDict)
        similarityColumn = self.getMetricColumns(peleControlFileDict)
        reportWildcard, trajWildcard = utilities.getReportAndTrajectoryWildcard(peleControlFileDict)

        for i, structure in enumerate(initialStructures):
            equilibrationOutput = os.path.join(outputPath, "equilibration_%d" % (i+1))
            equilibrationControlFile = outputPathConstants.tmpControlFilenameEqulibration % (i+1)
            utilities.makeFolder(equilibrationOutput)
            shutil.copyfile(structure, outputPathConstants.tmpInitialStructuresEquilibrationTemplate % (i+1))
            initialStructureString = self.createMultipleComplexesFilenames(1, outputPathConstants.tmpInitialStructuresEquilibrationTemplate, i+1, equilibration=True)
            equilibrationPeleDict["OUTPUT_PATH"] = equilibrationOutput
            equilibrationPeleDict["COMPLEXES"] = initialStructureString
            equilibrationPeleDict["BOX_CENTER"] = self.selectInitialBoxCenter(structure, resname)
            equilibrationPeleDict["BOX_RADIUS"] = 2
            for name in ["BOX_CENTER", "BOX_RADIUS"]:
                # If the template PELE control file is not templetized with the
                # box information, include it manually
                if name not in templateNames:
                    templateNames[name] = '"$%s"' % name
            print("Running equilibration for initial structure number %d" % (i+1))
            peleControlString = json.dumps(peleControlFileDict, indent=4)
            for key, value in templateNames.items():
                # Remove double quote around template keys, so that PELE
                # understands the options
                peleControlString = peleControlString.replace(value, "$%s" % key)

            self.makeWorkingControlFile(equilibrationControlFile, equilibrationPeleDict, peleControlString)
            self.runSimulation(equilibrationControlFile)
            # Extract report, trajnames, metrics columns from pele control file
            reportNames = os.path.join(equilibrationOutput, reportWildcard)
            trajNames = os.path.join(equilibrationOutput, trajWildcard)
            if len(initialStructures) == 1 and self.parameters.equilibrationMode == blockNames.SimulationParams.equilibrationLastSnapshot:
                newStructure.extend(self.selectEquilibrationLastSnapshot(self.parameters.processors, trajNames, topology=topologies.topologies[i]))
            elif self.parameters.equilibrationMode == blockNames.SimulationParams.equilibrationSelect:
                newStructure.extend(self.selectEquilibratedStructure(self.parameters.processors, similarityColumn, resname, trajNames, reportNames, topology=topologies.topologies[i]))
            elif self.parameters.equilibrationMode == blockNames.SimulationParams.equilibrationCluster:
                newStructure.extend(self.clusterEquilibrationStructures(resname, trajNames, reportNames, topology=topologies.topologies[i]))

        if len(newStructure) > (self.processors-1):
            # if for some reason the number of selected structures exceeds
            # the number of available processors, randomly sample the initial
            # structures
            newStructure = np.random.choice(newStructure, self.processors-1, replace=False)
        for j, struct in enumerate(newStructure):
            newStructurePath = os.path.join(equilibrationOutput, 'equilibration_struc_%d_%d.pdb' % (i+1, j+1))
            with open(newStructurePath, "w") as fw:
                fw.write(struct)
            newInitialStructures.append(newStructurePath)
        return newInitialStructures

    def clusterEquilibrationStructures(self, resname, trajWildcard, reportWildcard, topology=None):
        """
            Cluster the equilibration run

            :param resname: Name of the ligand in the pdb
            :type resname: str
            :param trajWildcard: Templetized path to trajectory files"
            :type trajWildcard: str
            :param reportWildcard: Templetized path to report files"
            :type reportWildcard: str
            :param topology: Topology for non-pdb trajectories
            :type topology: list

            :returns: list -- List with the pdb snapshots of the representatives structures
        """
        if not SKLEARN:
            raise utilities.UnsatisfiedDependencyException("No installation of scikit-learn found. Please, install scikit-learn or select a different equilibrationMode.")
        energyColumn = 3
        # detect number of trajectories available
        nTrajs = len(glob.glob(trajWildcard.rsplit("_", 1)[0]+"*"))+1
        data = []
        for i in range(1, nTrajs):
            report = np.loadtxt(reportWildcard % i)
            if len(report.shape) < 2:
                report = report[np.newaxis, :]
            snapshots = utilities.getSnapshots(trajWildcard % i)
            for nSnap, (line, snapshot) in enumerate(zip(report, snapshots)):
                conformation = atomset.PDB()
                conformation.initialise(snapshot, resname=resname, topology=topology)
                com = conformation.getCOM()
                data.append([line[energyColumn], i, nSnap]+com)
        data = np.array(data)
        data = data[data[:, 0].argsort()]
        nPoints = max(self.parameters.numberEquilibrationStructures, data.shape[0]//4)
        data = data[:nPoints]
        n_clusters = min(self.parameters.numberEquilibrationStructures, data.shape[0])
        kmeans = KMeans(n_clusters=n_clusters).fit(data[:, 3:])
        print("Clustered equilibration output into %d clusters!" % n_clusters)
        clustersInfo = {x: {"structure": None, "minDist": 1e6} for x in range(self.parameters.numberEquilibrationStructures)}
        for conf, cluster in zip(data, kmeans.labels_):
            dist = np.linalg.norm(kmeans.cluster_centers_[cluster]-conf[3:])
            if dist < clustersInfo[cluster]["minDist"]:
                clustersInfo[cluster]["minDist"] = dist
                clustersInfo[cluster]["structure"] = tuple(conf[1:3].astype(int))
        initialStructures = []
        for cl in range(self.parameters.numberEquilibrationStructures):
            if clustersInfo[cl]["structure"] is None:
                # If a cluster has no structure assigned, skip it
                continue
            traj, snap = clustersInfo[cl]["structure"]
            conf = utilities.getSnapshots(trajWildcard % traj)[snap]
            if not isinstance(conf, basestring):
                conf = utilities.get_mdtraj_object_PDBstring(conf, topology)
            initialStructures.append(conf)
        return initialStructures

    def selectEquilibrationLastSnapshot(self, nTrajs, trajWildcard, topology=None):
        """
            Select the last snapshot of each trajectory as a  representative
            initial structure from the equilibration run

            :param nTrajs: Number of trajectories
            :type nTrajs: int
            :param trajWildcard: Templetized path to trajectory files"
            :type trajWildcard: str
            :param topology: Topology for non-pdb trajectories
            :type topology: list

            :returns: list -- List with the pdb snapshots of the representatives structures
        """
        initialStructures = []
        for ij in range(1, nTrajs):
            conf = utilities.getSnapshots(trajWildcard % ij)[-1]
            if not isinstance(conf, basestring):
                conf = utilities.get_mdtraj_object_PDBstring(conf, topology)
            initialStructures.append(conf)

        return initialStructures

    def selectEquilibratedStructure(self, nTrajs, similarityColumn, resname, trajWildcard, reportWildcard, topology=None):
        """
            Select a representative initial structure from the equilibration
            run

            :param nTrajs: Number of trajectories
            :type nTrajs: int
            :param similarityColumn: Column number of the similarity metric
                (RMSD or distance)
            :type similarityColumn: int
            :param resname: Name of the ligand in the pdb
            :type resname: str
            :param trajWildcard: Templetized path to trajectory files"
            :type trajWildcard: str
            :param reportWildcard: Templetized path to report files"
            :type reportWildcard: str
            :param topology: Topology for non-pdb trajectories
            :type topology: list

            :returns: list -- List with the pdb snapshots of the representatives structures
        """
        energyColumn = 3
        values = []
        indices = []
        rowIndex = 0
        if similarityColumn is None:
            RMSDCalc = RMSDCalculator.RMSDCalculator()
            initial = atomset.PDB()
        else:
            cols = sorted([energyColumn, similarityColumn])

        for i in range(1, nTrajs):
            indices.append(rowIndex)
            report = np.loadtxt(reportWildcard % i)
            if len(report.shape) < 2:
                report = report[np.newaxis, :]
            if similarityColumn is None:
                snapshots = utilities.getSnapshots(trajWildcard % i)
                report_values = []
                if i == 1:
                    initial.initialise(snapshots.pop(0), resname=resname, topology=topology)
                    report_values.append([0, report[0, energyColumn]])
                    report = report[1:, :]
                for j, snap in enumerate(snapshots):
                    pdbConformation = atomset.PDB()
                    pdbConformation.initialise(snap, resname=resname, topology=topology)
                    report_values.append([RMSDCalc.computeRMSD(initial, pdbConformation), report[j, energyColumn]])
            else:
                report_values = report[:, cols]
            values.extend(report_values)
            rowIndex += len(report_values)

        values = np.array(values)
        if energyColumn > similarityColumn or similarityColumn is None:
            similarityColumn, energyColumn = list(range(2))
        else:
            energyColumn, similarityColumn = list(range(2))
        maxEnergy = values.max(axis=0)[energyColumn]
        # Substract the max value so all values will be negative (avoid sign problems)
        values[:, energyColumn] -= maxEnergy
        minEnergy = values.min(axis=0)[energyColumn]
        # Normalize to the minimum value
        values[:, energyColumn] /= minEnergy
        freq, bins = np.histogram(values[:, similarityColumn])
        freq = np.divide(freq, np.float(np.sum(freq)))
        # Get center of the bins
        centers = (bins[:-1]+bins[1:])/2.0
        for row in values:
            row[similarityColumn] = freq[np.argmin(np.abs(row[similarityColumn] - centers))]
        distance = values.sum(axis=1)
        indexSelected = np.argmax(distance)
        # Get trajectory and snapshot number from the index selected
        trajNum = len(indices)-1
        for i, index in enumerate(indices):
            if index == indexSelected:
                trajNum = i
                break
            elif indexSelected < index:
                trajNum = i-1
                break
        snapshotNum = indexSelected-indices[trajNum]
        # trajectories are 1-indexed
        trajNum += 1
        # return as list for compatibility with selectEquilibrationLastSnapshot
        conf = utilities.getSnapshots(trajWildcard % trajNum)[snapshotNum]
        if not isinstance(conf, basestring):
            conf = utilities.get_mdtraj_object_PDBstring(conf, topology)
        return [conf]

    def createMultipleComplexesFilenames(self, numberOfSnapshots, tmpInitialStructuresTemplate, iteration, equilibration=False):
        """
            Creates the string to substitute the complexes in the PELE control file

            :param numberOfSnapshots: Number of complexes to write
            :type numberOfSnapshots: int
            :param tmpInitialStructuresTemplate: Template with the name of the initial strutctures
            :type tmpInitialStructuresTemplate: str
            :param iteration: Epoch number
            :type iteration: int
            :param equilibration: Flag to mark wether the complexes are part of an
                equilibration run
            :type equilibration: bool

            :returns: str -- jsonString to be substituted in PELE control file
        """
        jsonString = ["\n"]
        for i in range(numberOfSnapshots-1):
            if equilibration:
                jsonString.append(constants.inputFileTemplate % (tmpInitialStructuresTemplate % (iteration)) + ",\n")
            else:
                jsonString.append(constants.inputFileTemplate % (tmpInitialStructuresTemplate % (iteration, i)) + ",\n")
        if equilibration:
            jsonString.append(constants.inputFileTemplate % (tmpInitialStructuresTemplate % (iteration)))
        else:
            jsonString.append(constants.inputFileTemplate % (tmpInitialStructuresTemplate % (iteration, numberOfSnapshots-1)))
        return "".join(jsonString)


class MDSimulation(SimulationRunner):
    def __init__(self, parameters):
        SimulationRunner.__init__(self, parameters)
        self.type = simulationTypes.SIMULATION_TYPE.MD
        self.antechamberTemplate = constants.AmberTemplates.antechamberTemplate
        self.parmchkTemplate = constants.AmberTemplates.parmchk2Template
        self.tleapTemplate = constants.AmberTemplates.tleapTemplate
        self.prmtopFiles = []
        self.ligandName = ""
        if not OPENMM:
            raise utilities.UnsatisfiedDependencyException("No installation of OpenMM found. Please, install OpenMM to run MD simulations.")

    def getWorkingProcessors(self):
        """
            Return the number of working processors, i.e. number of trajectories
        """
        return self.parameters.processors

    def equilibrate(self, initialStructures, outputPathConstants, reportFilename, outputPath, resname, topology=None):
        """
            Run short simulation to equilibrate the system. It will run one
            such simulation for every initial structure

            :param initialStructures: Name of the initial structures to copy
            :type initialStructures: list of str
            :param outputPathConstants: Contains outputPath-related constants
            :type outputPathConstants: :py:class:`.OutputPathConstants`
            :param reportBaseFilename: Name of the file that contains the metrics of the snapshots to cluster
            :type reportBaseFilename: str
            :param outputPath: Path where trajectories are found
            :type outputPath: str
            :param resname: Residue name of the ligand in the system pdb
            :type resname: str
            :param topology: Topology object
            :type topology: :py:class:

            :returns: list -- List with initial structures
        """
        self.ligandName = resname
        newInitialStructures = []
        solvatedStrcutures = []
        equilibrationFiles = []
        equilibrationOutput = os.path.join(outputPath, "equilibration")
        utilities.makeFolder(equilibrationOutput)
        # AmberTools generates intermediate files in the current directory, change to the tmp folder
        workingdirectory = os.getcwd()
        os.chdir(outputPathConstants.tmpFolder)
        ligandPDB = self.extractLigand(initialStructures[0], resname, outputpath="")
        ligandmol2 = "%s.mol2" % resname
        ligandfrcmod = "%s.frcmod" % resname
        Tleapdict = {"RESNAME": resname, "BOXSIZE": self.parameters.boxRadius, "MOL2": ligandmol2, "FRCMOD": ligandfrcmod}
        antechamberDict = {"LIGAND": ligandPDB, "OUTPUT": ligandmol2, "CHARGE": self.parameters.ligandCharge}
        parmchkDict = {"MOL2": ligandmol2, "OUTPUT": ligandfrcmod}
        self.prepareLigand(antechamberDict, parmchkDict)

        for i, structure in enumerate(initialStructures):
            TleapControlFile = "tleap_equilibration_%d.in" % (i + 1)
            prmtop = os.path.join(workingdirectory, equilibrationOutput, "system_%d.prmtop" % (i + 1))
            inpcrd = os.path.join(workingdirectory, equilibrationOutput, "system_%d.inpcrd" % (i + 1))
            finalPDB = os.path.join(workingdirectory, equilibrationOutput, "system_%d.pdb" % (i + 1))
            Tleapdict["COMPLEX"] = structure
            Tleapdict["PRMTOP"] = prmtop
            Tleapdict["INPCRD"] = inpcrd
            Tleapdict["SOLVATED_PDB"] = finalPDB
            self.makeWorkingControlFile(TleapControlFile, Tleapdict, self.tleapTemplate)
            self.runTleap(TleapControlFile)
            solvatedStrcutures.append(finalPDB)
            self.prmtopFiles.append(prmtop)
            equilibrationFiles.append((prmtop, inpcrd))

        os.chdir(workingdirectory)
        pool = mp.Pool(min(self.getWorkingProcessors(), len(equilibrationFiles)))
        workers = []
        startTime = time.time()
        print("equilibrating System")
        for i, equilibrationFilePair in enumerate(equilibrationFiles):
            outputPDB = os.path.join(equilibrationOutput, "equilibrated_system_%d.pdb" % (i + 1))
            workers.append(pool.apply_async(self.runEquilibration, args=(equilibrationFilePair, outputPDB)))

        for worker in workers:
            newInitialStructures.append(worker.get())
        endTime = time.time()
        print("Equilibration took %.2f sec" % (endTime - startTime))
        return newInitialStructures

    def runTleap(self, TleapControlFile):
        tleapCommand = "tleap -f %s" % TleapControlFile
        print("System Preparation")
        startTime = time.time()
        proc = subprocess.Popen(tleapCommand, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        (out, err) = proc.communicate()
        print(out)
        if err:
            print(err)
        endTime = time.time()
        print("System preparation took %.2f sec" % (endTime - startTime))

    def preparePDB(self, PDBtoOpen, outputpath):
        """
        Corrects problems in the pdb such as CONECT and wrong histidine codes

        :param PDBtoOpen: string with the pdb to prepare
        :type PDBtoOpen: str
        :param outputPath: Path where the pdb is written
        :type outputPath: str
        """
        pass

    def extractLigand(self, PDBtoOpen, resname, outputpath):
        """
            Extracts the ligand from a given PDB

            :param PDBtoOpen: string with the pdb to prepare
            :type PDBtoOpen: str
            :param resname: string with the code of the ligand
            :type resname: str
            :param outputPath: Path where the pdb is written
            :type outputPath: str

            :returns: str -- string with the ligand pdb
        """
        ligandpdb = os.path.join(outputpath, "raw_ligand.pdb")
        with open(ligandpdb, "w") as out:
            with open(PDBtoOpen, "r") as inp:
                for line in inp:
                    if resname in line:
                        out.write(line)
        return ligandpdb

    def prepareLigand(self, antechamberDict, parmchkDict):
        """
        Runs antechamber and parmchk2 to obtain the mol2 and frcmod of the ligand

        :param antechamberDict: Dictonary containing the parameters to substitute in the antechamber command
        :type antechamberDict: dict
        :param parmchkDict: Dictonary containing the parameters to substitute in the parmchk2 command
        :type parmchkDict: dict
        """
        antechamberCommand = string.Template(self.antechamberTemplate)
        antechamberCommand = antechamberCommand.substitute(antechamberDict)
        parmchkCommand = string.Template(self.parmchkTemplate)
        parmchkCommand = parmchkCommand.substitute(parmchkDict)
        print(antechamberCommand)
        startTime = time.time()
        proc = subprocess.Popen(antechamberCommand, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        (out, err) = proc.communicate()
        print(out)
        if err:
            print(err)
        print(parmchkCommand)
        proc = subprocess.Popen(parmchkCommand, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        (out, err) = proc.communicate()
        print(out)
        if err:
            print(err)
        endTime = time.time()
        print("Ligand preparation took %.2f sec" % (endTime - startTime))

    def runEquilibration(self, equilibrationFiles, outputPDB):
        """
            Function that runs the whole equilibration process and returns the final pdb

            :param equilibrationFiles: tuple with the topology (prmtop) in the first position and the coordinates
            in the second (inpcrd)
            :param outputPDB: string with the pdb to save

            :returns: str -- a string with the outputPDB
        """
        prmtop, inpcrd = equilibrationFiles
        prmtop = app.AmberPrmtopFile(prmtop)
        inpcrd = app.AmberInpcrdFile(inpcrd)
        PLATFORM = mm.Platform_getPlatformByName(self.parameters.runningPlatform)
        simulation = self.minimization(prmtop, inpcrd, PLATFORM, constraints=5)
        positions = simulation.context.getState(getPositions=True).getPositions()
        velocities = simulation.context.getState(getVelocities=True).getVelocities()
        simulation = self.NVTequilibration(prmtop, positions, PLATFORM, simulation_steps=self.parameters.equilibrationLength, constraints=5, velocities=velocities)
        positions = simulation.context.getState(getPositions=True).getPositions()
        velocities = simulation.context.getState(getVelocities=True).getVelocities()
        simulation = self.NPTequilibration(prmtop, positions, PLATFORM, simulation_steps=self.parameters.equilibrationLength, constraints=0.5, velocities=velocities)
        with open(outputPDB, 'w') as fw:
            app.PDBFile.writeFile(simulation.topology, simulation.context.getState(getPositions=True).getPositions(), fw)
        return outputPDB

    def minimization(self, prmtop, inpcrd, PLATFORM, constraints):
        # Thermostat
        system = prmtop.createSystem(nonbondedMethod=app.PME,
                                     nonbondedCutoff=self.parameters.nonBondedCutoff * unit.angstroms, constraints=app.HBonds)
        # system.addForce(mm.AndersenThermostat(self.parameters.Temperature * unit.kelvin, 1 / unit.picosecond))
        integrator = mm.VerletIntegrator(2 * unit.femtoseconds)
        if constraints:
            # Add positional restraints to protein backbone
            force = mm.CustomExternalForce("k*((x-x0)^2+(y-y0)^2+(z-z0)^2)")
            force.addGlobalParameter("k", constraints * unit.kilocalories_per_mole / unit.angstroms ** 2)
            force.addPerParticleParameter("x0")
            force.addPerParticleParameter("y0")
            force.addPerParticleParameter("z0")
            for j, atom in enumerate(prmtop.topology.atoms()):
                if (atom.name in ('CA', 'C', 'N', 'O') and atom.residue.name != "HOH") or (
                        atom.residue.name == self.ligandName and atom.element.symbol != "H"):
                    force.addParticle(j, inpcrd.positions[j].value_in_unit(unit.nanometers))
            system.addForce(force)

        simulation = app.Simulation(prmtop.topology, system, integrator, PLATFORM)
        if inpcrd.boxVectors is not None:
            simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)
        simulation.context.setPositions(inpcrd.positions)
        simulation.minimizeEnergy(maxIterations=self.parameters.minimizationIterations)
        return simulation

    def NVTequilibration(self, topology, positions, PLATFORM, simulation_steps, constraints, velocities=None):
        system = topology.createSystem(nonbondedMethod=app.PME,
                                       nonbondedCutoff=self.parameters.nonBondedCutoff * unit.angstroms,
                                       constraints=app.HBonds)
        system.addForce(mm.AndersenThermostat(self.parameters.Temperature * unit.kelvin, 1 / unit.picosecond))
        integrator = mm.VerletIntegrator(2 * unit.femtoseconds)
        if constraints:
            force = mm.CustomExternalForce("k*((x-x0)^2+(y-y0)^2+(z-z0)^2)")
            force.addGlobalParameter("k", constraints * unit.kilocalories_per_mole / unit.angstroms ** 2)
            force.addPerParticleParameter("x0")
            force.addPerParticleParameter("y0")
            force.addPerParticleParameter("z0")
            for j, atom in enumerate(topology.topology.atoms()):
                if (atom.name in ('CA', 'C', 'N', 'O') and atom.residue.name != "HOH") or (atom.residue.name == self.ligandName and atom.element.symbol != "H"):
                    force.addParticle(j, positions[j].value_in_unit(unit.nanometers))
            system.addForce(force)
        simulation = app.Simulation(topology.topology, system, integrator, PLATFORM)
        simulation.context.setPositions(positions)
        if velocities:
            simulation.context.setVelocities(velocities)
        else:
            simulation.context.setVelocitiesToTemperature(self.parameters.Temperature * unit.kelvin, 1)
        simulation.step(simulation_steps)
        return simulation

    def NPTequilibration(self, topology, positions, PLATFORM, simulation_steps, constraints, velocities=None):
        system = topology.createSystem(nonbondedMethod=app.PME,
                                       nonbondedCutoff=self.parameters.nonBondedCutoff * unit.angstroms,
                                       constraints=app.HBonds)
        system.addForce(mm.AndersenThermostat(self.parameters.Temperature * unit.kelvin, 1 / unit.picosecond))
        integrator = mm.VerletIntegrator(2 * unit.femtoseconds)
        system.addForce(mm.MonteCarloBarostat(1 * unit.bar, self.parameters.Temperature * unit.kelvin))
        if constraints:
            force = mm.CustomExternalForce("k*((x-x0)^2+(y-y0)^2+(z-z0)^2)")
            force.addGlobalParameter("k", constraints * unit.kilocalories_per_mole / unit.angstroms ** 2)
            force.addPerParticleParameter("x0")
            force.addPerParticleParameter("y0")
            force.addPerParticleParameter("z0")
            for j, atom in enumerate(topology.topology.atoms()):
                if atom.name == 'CA' or (atom.residue.name == self.ligandName and atom.element.symbol != "H"):
                    force.addParticle(j, positions[j].value_in_unit(unit.nanometers))
            system.addForce(force)
        simulation = app.Simulation(topology.topology, system, integrator, PLATFORM)
        simulation.context.setPositions(positions)
        if velocities:
            simulation.context.setVelocities(velocities)
        else:
            simulation.context.setVelocitiesToTemperature(self.parameters.Temperature * unit.kelvin, 1)
        simulation.step(simulation_steps)
        return simulation

    def runSimulation(self, epoch, outputPathConstants, initialStructuresAsString, topologies):
        # change signature
        outputDir = outputPathConstants.epochOutputPathTempletized % epoch
        processors = self.getWorkingProcessors()
        structures_to_run = initialStructuresAsString.split(":")
        startingFilesPairs = [(self.prmtopFiles[topologies.getTopologyIndex(epoch, i)], structure)
                              for i, structure in enumerate(structures_to_run)]
        print("Starting OpenMM Production Run...")
        startTime = time.time()
        pool = mp.Pool(self.getWorkingProcessors())
        workers = []
        for i, startingFiles in zip(range(processors), itertools.cycle(startingFilesPairs)):
            workerNumber = i + 1
            seed = self.parameters.seed + epoch * self.parameters.processors
            workers.append(pool.apply_async(self.MDsimulationRunner, args=(startingFiles, workerNumber, outputDir, seed)))
        for worker in workers:
            worker.get()
        endTime = time.time()
        print("OpenMM took %.2f sec" % (endTime - startTime))

    def MDsimulationRunner(self, equilibrationFiles, workerNumber, outputDir, seed):
        prmtop, pdb = equilibrationFiles
        prmtop = app.AmberPrmtopFile(prmtop)
        PDBrepoter = os.path.join(outputDir, constants.AmberTemplates.trajectoryTemplate % workerNumber)
        stateReporter = os.path.join(outputDir, constants.AmberTemplates.StateDataReporterTemplate % workerNumber)
        pdb = app.PDBFile(pdb)
        PLATFORM = mm.Platform_getPlatformByName(self.parameters.runningPlatform)
        system = prmtop.createSystem(nonbondedMethod=app.PME,
                                     nonbondedCutoff=self.parameters.nonBondedCutoff * unit.angstroms,
                                     constraints=app.HBonds)
        system.addForce(mm.AndersenThermostat(self.parameters.Temperature * unit.kelvin, 1 / unit.picosecond))
        integrator = mm.VerletIntegrator(2 * unit.femtoseconds)
        simulation = app.Simulation(prmtop.topology, system, integrator, PLATFORM)
        simulation.context.setPositions(pdb.positions)
        simulation.context.setVelocitiesToTemperature(self.parameters.Temperature * unit.kelvin, seed)
        simulation.reporters.append(app.PDBReporter(PDBrepoter, self.parameters.reporterFreq, enforcePeriodicBox=True))
        if self.parameters.energyReport:
            simulation.reporters.append(app.StateDataReporter(stateReporter, self.parameters.reporterFreq, step=True, potentialEnergy=True,
                                                              temperature=True, time=True, volume=True,
                                                              remainingTime=True, speed=True, totalSteps=self.parameters.productionLength, separator="\t"))
        if workerNumber == 1:
            frequency = min(10 * self.parameters.reporterFreq, self.parameters.productionLength)
            simulation.reporters.append(app.StateDataReporter(sys.stdout, frequency, step=True))
        simulation.step(self.parameters.productionLength)

    def createMultipleComplexesFilenames(self, numberOfSnapshots, tmpInitialStructuresTemplate, iteration, equilibration=False):
        """
            Creates the string to substitute the complexes in the PELE control file

            :param numberOfSnapshots: Number of complexes to write
            :type numberOfSnapshots: int
            :param tmpInitialStructuresTemplate: Template with the name of the initial strutctures
            :type tmpInitialStructuresTemplate: str
            :param iteration: Epoch number
            :type iteration: int
            :param equilibration: Flag to mark wether the complexes are part of an
                equilibration run
            :type equilibration: bool

            :returns: str with the files to be used
        """
        initialStructures = []
        for i in range(numberOfSnapshots-1):
            initialStructures.append(tmpInitialStructuresTemplate % (iteration, i)+":")
        initialStructures.append((tmpInitialStructuresTemplate % (iteration, numberOfSnapshots-1)))
        return "".join(initialStructures)

    def checkSimulationInterrupted(self, epoch):
        """
            Check wether the simulation was interrupted before finishing

            :param epoch: Epoch number
            :type epoch: int

            :returns: bool -- True if the simulations where interrupted
        """
        # to be implemented depending on implementation details
        pass

    def cleanCheckpointFiles(self, epoch):
        """
            Clean the restart files generated if the simulation was interrupted
            before finishing

            :param epoch: Epoch number
            :type epoch: int
        """
        # to be implemented depending on implementation details
        pass


class TestSimulation(SimulationRunner):
    """
        Class used for testing
    """
    def __init__(self, parameters):
        SimulationRunner.__init__(self, parameters)
        self.type = simulationTypes.SIMULATION_TYPE.TEST
        self.copied = False
        self.parameters = parameters

    def getWorkingProcessors(self):
        """
            Return the number of working processors, i.e. number of trajectories
        """
        return self.parameters.processors-1

    def runSimulation(self, epoch, outputPathConstants, initialStructuresAsString, topologies):
        """
            Copy file to test the rest of the AdaptivePELE procedure
        """
        ControlFileDictionary = {"COMPLEXES": initialStructuresAsString,
                                 "PELE_STEPS": self.parameters.peleSteps,
                                 "BOX_RADIUS": self.parameters.boxRadius}
        self.prepareControlFile(epoch, outputPathConstants, ControlFileDictionary)
        if not self.copied:
            if os.path.exists(self.parameters.destination):
                shutil.rmtree(self.parameters.destination)
            shutil.copytree(self.parameters.origin, self.parameters.destination)
            self.copied = True

    def makeWorkingControlFile(self, workingControlFilename, dictionary, inputTemplate=None):
        pass


class ClusteringExitCondition:
    def __init__(self, ntrajs):
        self.clusterNum = 0
        self.ntrajs = ntrajs
        self.type = simulationTypes.EXITCONDITION_TYPE.CLUSTERING

    def checkExitCondition(self, clustering):
        """
            Iterate over all unchecked cluster and check if the exit condtion
            is met

            :param clustering: Clustering object
            :type clustering: :py:class:`.Clustering`

            :returns: bool -- Returns True if the exit condition has been met
        """
        newClusterNum = clustering.getNumberClusters()
        clusterDiff = newClusterNum - self.clusterNum
        self.clusterNum = newClusterNum
        return clusterDiff < 0.1*self.ntrajs


class MetricExitCondition:
    def __init__(self, metricCol, metricValue, condition):
        self.metricCol = metricCol
        self.metricValue = metricValue
        self.type = simulationTypes.EXITCONDITION_TYPE.METRIC
        if condition == ">":
            self.condition = lambda x, y: x > y
        else:
            self.condition = lambda x, y: x < y

    def checkExitCondition(self, clustering):
        """
            Iterate over all clusters and check if the exit condtion
            is met

            :param clustering: Clustering object
            :type clustering: :py:class:`.Clustering`

            :returns: bool -- Returns True if the exit condition has been met
        """
        for cluster in clustering.clusters.clusters:
            metric = cluster.getMetricFromColumn(self.metricCol)

            if metric is not None and self.condition(metric, self.metricValue):
                return True
        return False


class MetricMultipleTrajsExitCondition:
    def __init__(self, metricCol, metricValue, condition, reportWildCard, numTrajs, nProcessors):
        self.metricCol = metricCol
        self.metricValue = metricValue
        self.type = simulationTypes.EXITCONDITION_TYPE.METRICMULTIPLETRAJS
        self.numTrajs = numTrajs
        self.nProcessors = nProcessors
        self.trajsFound = 0
        if condition == ">":
            self.condition = lambda x, y: x.max() > y
        else:
            self.condition = lambda x, y: x.min() < y
        self.report = reportWildCard

    def checkExitCondition(self, outputFolder):
        """
            Iterate over all reports and check if the exit condtion
            is met

            :param clustering: Clustering object
            :type clustering: :py:class:`.Clustering`

            :returns: bool -- Returns True if the exit condition has been met
        """
        for j in range(1, self.nProcessors):
            report = np.loadtxt(os.path.join(outputFolder, self.report % j))
            if len(report.shape) < 2:
                # If a report has only one line, add another axis
                report = report[None]
            if self.condition(report[:, self.metricCol], self.metricValue):
                self.trajsFound += 1
        return self.trajsFound >= self.numTrajs


class RunnerBuilder:
    def build(self, simulationRunnerBlock):
        """
            Build the selected  SimulationRunner object

            :param simulationRunnerBlock: Block of the control file
                corresponding to the simulation step
            :type simulationRunnerBlock: dict

            :returns: :py:class:`.SimulationRunner` -- SimulationRunner object
                selected
        """
        simulationType = simulationRunnerBlock[blockNames.SimulationType.type]
        paramsBlock = simulationRunnerBlock[blockNames.SimulationParams.params]
        params = SimulationParameters()
        if simulationType == blockNames.SimulationType.pele:
            params.processors = paramsBlock[blockNames.SimulationParams.processors]
            params.dataFolder = paramsBlock.get(blockNames.SimulationParams.dataFolder, constants.DATA_FOLDER)
            params.documentsFolder = paramsBlock.get(blockNames.SimulationParams.documentsFolder, constants.DOCUMENTS_FOLDER)
            params.executable = paramsBlock.get(blockNames.SimulationParams.executable, constants.PELE_EXECUTABLE)
            params.templetizedControlFile = paramsBlock[blockNames.SimulationParams.templetizedControlFile]
            params.iterations = paramsBlock[blockNames.SimulationParams.iterations]
            params.peleSteps = paramsBlock[blockNames.SimulationParams.peleSteps]
            params.seed = paramsBlock[blockNames.SimulationParams.seed]
            params.modeMovingBox = paramsBlock.get(blockNames.SimulationParams.modeMovingBox)
            if params.modeMovingBox is not None:
                if params.modeMovingBox.lower() == blockNames.SimulationParams.modeMovingBoxBinding:
                    params.SASAforBox = 1.0
                elif params.modeMovingBox.lower() == blockNames.SimulationParams.modeMovingBoxUnBinding:
                    params.SASAforBox = 0.0
                peleDict, _ = utilities.getPELEControlFileDict(params.templetizedControlFile)
                params.reportName, params.trajectoryName = utilities.getReportAndTrajectoryWildcard(peleDict)
                params.columnSASA = utilities.getSASAcolumnFromControlFile(peleDict)
            params.boxCenter = paramsBlock.get(blockNames.SimulationParams.boxCenter)
            params.boxRadius = paramsBlock.get(blockNames.SimulationParams.boxRadius, 20)
            params.runEquilibration = paramsBlock.get(blockNames.SimulationParams.runEquilibration, False)
            params.equilibrationMode = paramsBlock.get(blockNames.SimulationParams.equilibrationMode, blockNames.SimulationParams.equilibrationSelect)
            params.equilibrationLength = paramsBlock.get(blockNames.SimulationParams.equilibrationLength)
            params.numberEquilibrationStructures = paramsBlock.get(blockNames.SimulationParams.numberEquilibrationStructures, 10)
            params.srun = paramsBlock.get(blockNames.SimulationParams.srun, False)
            exitConditionBlock = paramsBlock.get(blockNames.SimulationParams.exitCondition, None)
            if exitConditionBlock:
                exitConditionBuilder = ExitConditionBuilder()
                params.exitCondition = exitConditionBuilder.build(exitConditionBlock, params.templetizedControlFile, params.processors)

            return PeleSimulation(params)
        elif simulationType == blockNames.SimulationType.md:
            params.processors = paramsBlock[blockNames.SimulationParams.processors]
            params.iterations = paramsBlock[blockNames.SimulationParams.iterations]
            params.runEquilibration = True
            params.ligandCharge = paramsBlock.get(blockNames.SimulationParams.ligandCharge, 1)
            params.nonBondedCutoff = paramsBlock.get(blockNames.SimulationParams.nonBondedCutoff, 8)
            params.boxRadius = paramsBlock.get(blockNames.SimulationParams.boxRadius, 8)
            params.Temperature = paramsBlock.get(blockNames.SimulationParams.Temperature, 300)
            params.runningPlatform = paramsBlock.get(blockNames.SimulationParams.runningPlatform, "CPU")
            params.minimizationIterations = paramsBlock.get(blockNames.SimulationParams.minimizationIterations, 2000)
            params.seed = paramsBlock[blockNames.SimulationParams.seed]
            params.reporterFreq = paramsBlock[blockNames.SimulationParams.repoterfreq]
            params.productionLength = paramsBlock[blockNames.SimulationParams.productionLength]
            params.equilibrationLength = paramsBlock.get(blockNames.SimulationParams.equilibrationLength, 4000)
            params.energyReport = paramsBlock.get(blockNames.SimulationParams.energyReport, True)

            return MDSimulation(params)
        elif simulationType == blockNames.SimulationType.test:
            params.processors = paramsBlock[blockNames.SimulationParams.processors]
            params.destination = paramsBlock[blockNames.SimulationParams.destination]
            params.origin = paramsBlock[blockNames.SimulationParams.origin]
            params.iterations = paramsBlock[blockNames.SimulationParams.iterations]
            params.peleSteps = paramsBlock[blockNames.SimulationParams.peleSteps]
            params.seed = paramsBlock[blockNames.SimulationParams.seed]
            return TestSimulation(params)
        else:
            sys.exit("Unknown simulation type! Choices are: " + str(simulationTypes.SIMULATION_TYPE_TO_STRING_DICTIONARY.values()))


class ExitConditionBuilder:
    def build(self, exitConditionBlock, templetizedControlFile, nProcessors):
        """
            Build the selected exit condition object

            :param exitConditionBlock: Block of the control file
                corresponding to the exit condition
            :type exitConditionBlock: dict

            :returns: :py:class:`.MetricExitCondition` -- MetricExitCondition object
                selected
        """
        exitConditionType = exitConditionBlock[blockNames.ExitConditionType.type]
        exitConditionParams = exitConditionBlock[blockNames.SimulationParams.params]
        if exitConditionType == blockNames.ExitConditionType.metric:
            # Start counting the columns by 1
            metricCol = exitConditionParams[blockNames.SimulationParams.metricCol]-1
            metricValue = exitConditionParams[blockNames.SimulationParams.exitValue]
            condition = exitConditionParams.get(blockNames.SimulationParams.condition, "<")
            if condition not in [">", "<"]:
                raise ValueError("In MetricExitCondition the parameter condition only accepts > or <, but %s was passed" % condition)
            return MetricExitCondition(metricCol, metricValue, condition)
        elif exitConditionType == blockNames.ExitConditionType.metricMultipleTrajs:
            # Start counting the columns by 1
            metricCol = exitConditionParams[blockNames.SimulationParams.metricCol]-1
            metricValue = exitConditionParams[blockNames.SimulationParams.exitValue]
            numTrajs = exitConditionParams[blockNames.SimulationParams.numTrajs]
            condition = exitConditionParams.get(blockNames.SimulationParams.condition, "<")
            if condition not in [">", "<"]:
                raise ValueError("In MetricMultipleTrajsExitCondition the parameter condition only accepts > or <, but %s was passed" % condition)
            peleControlFileDict, _ = utilities.getPELEControlFileDict(templetizedControlFile)
            reportWildCard, _ = utilities.getReportAndTrajectoryWildcard(peleControlFileDict)
            return MetricMultipleTrajsExitCondition(metricCol, metricValue, condition, reportWildCard, numTrajs, nProcessors)
        elif exitConditionType == blockNames.ExitConditionType.clustering:
            ntrajs = exitConditionParams[blockNames.SimulationParams.trajectories]
            return ClusteringExitCondition(ntrajs)
        else:
            sys.exit("Unknown exit condition type! Choices are: " + str(simulationTypes.EXITCONDITION_TYPE_TO_STRING_DICTIONARY.values()))
