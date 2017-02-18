Search.setIndex({envversion:49,filenames:["AdaptiveSampling","Examples","index","src.analysis","src.atomset","src.clustering","src.simulation","src.spawning","src.utilities","src.validator"],objects:{"src.adaptiveSampling":{buildNewClusteringAndWriteInitialStructuresInNewSimulation:[0,1,1,""],buildNewClusteringAndWriteInitialStructuresInRestart:[0,1,1,""],checkSymmetryDict:[0,1,1,""],clusterEpochTrajs:[0,1,1,""],clusterPreviousEpochs:[0,1,1,""],copyInitialStructures:[0,1,1,""],createMultipleComplexesFilenames:[0,1,1,""],findFirstRun:[0,1,1,""],fixReportsSymmetry:[0,1,1,""],generateSnapshotSelectionStringLastRound:[0,1,1,""],getWorkingClusteringObject:[0,1,1,""],loadParams:[0,1,1,""],main:[0,1,1,""],needToRecluster:[0,1,1,""],parseArgs:[0,1,1,""],preparePeleControlFile:[0,1,1,""],saveInitialControlFile:[0,1,1,""]},"src.analysis":{correctRMSD:[3,0,0,"-"],foldersFirstBindingEvent:[3,0,0,"-"],generateGnuplotFile:[3,0,0,"-"],makePNGs:[3,0,0,"-"],numberOfOwnClusters:[3,0,0,"-"],writeClusteringStructures:[3,0,0,"-"]},"src.analysis.correctRMSD":{extendReportWithRmsd:[3,1,1,""],main:[3,1,1,""],parseArguments:[3,1,1,""],readControlFile:[3,1,1,""]},"src.analysis.foldersFirstBindingEvent":{main:[3,1,1,""],parseArguments:[3,1,1,""]},"src.analysis.generateGnuplotFile":{generateForLoopString:[3,1,1,""],generateNestedString:[3,1,1,""],generatePrintString:[3,1,1,""],parseArguments:[3,1,1,""]},"src.analysis.makePNGs":{buildGnuplotString:[3,1,1,""]},"src.analysis.numberOfOwnClusters":{buildClustersPerValue:[3,1,1,""],findDifferentClustersForAllEpochs:[3,1,1,""],findDifferentClustersInEpoch:[3,1,1,""],getAllDifferentValues:[3,1,1,""],getClusteringSummaryContent:[3,1,1,""],getNumberOfClustersPerEpochForGivenColumn:[3,1,1,""],getTotalNumberOfClustersPerEpoch:[3,1,1,""],main:[3,1,1,""],plotClustersPerValue:[3,1,1,""],plotContactsHistogram:[3,1,1,""],printHelp:[3,1,1,""]},"src.analysis.writeClusteringStructures":{parseArgs:[3,1,1,""]},"src.atomset":{RMSDCalculator:[4,0,0,"-"],SymmetryContactMapEvaluator:[4,0,0,"-"],atomset:[4,0,0,"-"]},"src.atomset.RMSDCalculator":{RMSDCalculator:[4,2,1,""]},"src.atomset.RMSDCalculator.RMSDCalculator":{computeNonSymmAtoms:[4,3,1,""],computeRMSD2:[4,3,1,""],computeRMSD:[4,3,1,""]},"src.atomset.SymmetryContactMapEvaluator":{SymmetryContactMapEvaluator:[4,2,1,""],calculateCorrelationContactMaps:[4,1,1,""]},"src.atomset.SymmetryContactMapEvaluator.SymmetryContactMapEvaluator":{buildContactMap:[4,3,1,""],buildContactMapWithRowMap:[4,3,1,""],buildOptimalPermutationContactMap:[4,3,1,""],createContactMap:[4,3,1,""],evaluateCorrelation:[4,3,1,""],evaluateDifferenceDistance:[4,3,1,""],evaluateJaccard:[4,3,1,""]},"src.atomset.atomset":{Atom:[4,2,1,""],PDB:[4,2,1,""],computeCOMDifference:[4,1,1,""],computeCOMSquaredDifference:[4,1,1,""],computeSquaredCentroidDifference:[4,1,1,""],readPDB:[4,1,1,""]},"src.atomset.atomset.Atom":{getAtomCoords:[4,3,1,""],isHeavyAtom:[4,3,1,""],isHeteroAtom:[4,3,1,""],isProtein:[4,3,1,""],printAtom:[4,3,1,""],squaredDistance:[4,3,1,""]},"src.atomset.atomset.PDB":{computeTotalMass:[4,3,1,""],countContacts:[4,3,1,""],extractCOM:[4,3,1,""],extractCentroid:[4,3,1,""],getAtom:[4,3,1,""],getCOM:[4,3,1,""],getCentroid:[4,3,1,""],getNumberOfAtoms:[4,3,1,""],initialise:[4,3,1,""],printAtoms:[4,3,1,""],writePDB:[4,3,1,""]},"src.automateRoundsAdaptive":{automateSimulation:[0,1,1,""],main:[0,1,1,""],parseArguments:[0,1,1,""]},"src.clustering":{clustering:[5,0,0,"-"],clusteringTypes:[5,0,0,"-"],thresholdcalculator:[5,0,0,"-"],thresholdcalculatortypes:[5,0,0,"-"]},"src.clustering.clustering":{CMClusteringEvaluator:[5,2,1,""],Cluster:[5,2,1,""],Clustering:[5,2,1,""],ClusteringBuilder:[5,2,1,""],Clusters:[5,2,1,""],ContactMapAccumulativeClustering:[5,2,1,""],ContactMapAgglomerativeClustering:[5,2,1,""],ContactMapClustering:[5,2,1,""],ContactsClustering:[5,2,1,""],ContactsClusteringEvaluator:[5,2,1,""],JaccardEvaluator:[5,2,1,""],SequentialLastSnapshotClustering:[5,2,1,""],clusterAgglomerativeContactMaps:[5,1,1,""],clusterContactMaps:[5,1,1,""],clusterKmeans:[5,1,1,""],clusteringResultsParameters:[5,2,1,""],correlationEvaluator:[5,2,1,""],differenceDistanceEvaluator:[5,2,1,""],getAllTrajectories:[5,1,1,""],processSnapshots:[5,1,1,""],selectRandomCenter:[5,1,1,""],similarityEvaluatorBuilder:[5,2,1,""]},"src.clustering.clustering.CMClusteringEvaluator":{checkAttributes:[5,3,1,""],cleanContactMap:[5,3,1,""],getInnerLimit:[5,3,1,""],isElement:[5,3,1,""]},"src.clustering.clustering.Cluster":{addElement:[5,3,1,""],getContacts:[5,3,1,""],getMetric:[5,3,1,""],getMetricFromColumn:[5,3,1,""],printCluster:[5,3,1,""],writePDB:[5,3,1,""]},"src.clustering.clustering.Clustering":{addSnapshotToCluster:[5,3,1,""],cluster:[5,3,1,""],getCluster:[5,3,1,""],getNumberClusters:[5,3,1,""],setCol:[5,3,1,""],writeOutput:[5,3,1,""]},"src.clustering.clustering.ClusteringBuilder":{buildClustering:[5,3,1,""]},"src.clustering.clustering.Clusters":{addCluster:[5,3,1,""],getCluster:[5,3,1,""],getNumberClusters:[5,3,1,""],insertCluster:[5,3,1,""],printClusters:[5,3,1,""]},"src.clustering.clustering.ContactMapAgglomerativeClustering":{cluster:[5,3,1,""],processClusterResults:[5,3,1,""]},"src.clustering.clustering.ContactMapClustering":{cluster:[5,3,1,""],processClusterResults:[5,3,1,""]},"src.clustering.clustering.ContactsClusteringEvaluator":{checkAttributes:[5,3,1,""],cleanContactMap:[5,3,1,""],getInnerLimit:[5,3,1,""],isElement:[5,3,1,""]},"src.clustering.clustering.JaccardEvaluator":{isSimilarCluster:[5,3,1,""]},"src.clustering.clustering.SequentialLastSnapshotClustering":{addSnapshotToCluster:[5,3,1,""],cluster:[5,3,1,""]},"src.clustering.clustering.correlationEvaluator":{isSimilarCluster:[5,3,1,""]},"src.clustering.clustering.differenceDistanceEvaluator":{isSimilarCluster:[5,3,1,""]},"src.clustering.clustering.similarityEvaluatorBuilder":{build:[5,3,1,""]},"src.clustering.clusteringTypes":{CLUSTERING_TYPES:[5,2,1,""],SIMILARITY_TYPES:[5,2,1,""]},"src.clustering.clusteringTypes.CLUSTERING_TYPES":{contactMapAccumulative:[5,4,1,""],contactMapAffinity:[5,4,1,""],contactMapAgglomerative:[5,4,1,""],contacts:[5,4,1,""],lastSnapshot:[5,4,1,""]},"src.clustering.clusteringTypes.SIMILARITY_TYPES":{Jaccard:[5,4,1,""],correlation:[5,4,1,""],differenceDistance:[5,4,1,""]},"src.clustering.thresholdcalculator":{ThresholdCalculator:[5,2,1,""],ThresholdCalculatorBuilder:[5,2,1,""],ThresholdCalculatorConstant:[5,2,1,""],ThresholdCalculatorHeaviside:[5,2,1,""]},"src.clustering.thresholdcalculator.ThresholdCalculator":{calculate:[5,3,1,""]},"src.clustering.thresholdcalculator.ThresholdCalculatorBuilder":{build:[5,3,1,""]},"src.clustering.thresholdcalculator.ThresholdCalculatorConstant":{calculate:[5,3,1,""],getMaxThreshold:[5,3,1,""]},"src.clustering.thresholdcalculator.ThresholdCalculatorHeaviside":{calculate:[5,3,1,""],getMaxThreshold:[5,3,1,""]},"src.clustering.thresholdcalculatortypes":{THRESHOLD_CALCULATOR_TYPES:[5,2,1,""]},"src.clustering.thresholdcalculatortypes.THRESHOLD_CALCULATOR_TYPES":{constant:[5,4,1,""],heaviside:[5,4,1,""]},"src.simulation":{simulationTypes:[6,0,0,"-"],simulationrunner:[6,0,0,"-"]},"src.simulation.simulationTypes":{EXITCONDITION_TYPE:[6,2,1,""],SIMULATION_TYPE:[6,2,1,""]},"src.simulation.simulationTypes.EXITCONDITION_TYPE":{CLUSTERING:[6,4,1,""],METRIC:[6,4,1,""]},"src.simulation.simulationTypes.SIMULATION_TYPE":{MD:[6,4,1,""],PELE:[6,4,1,""],TEST:[6,4,1,""]},"src.simulation.simulationrunner":{ClusteringExitCondition:[6,2,1,""],ExitConditionBuilder:[6,2,1,""],MetricExitCondition:[6,2,1,""],PeleSimulation:[6,2,1,""],RunnerBuilder:[6,2,1,""],SimulationParameters:[6,2,1,""],SimulationRunner:[6,2,1,""],TestSimulation:[6,2,1,""]},"src.simulation.simulationrunner.ClusteringExitCondition":{checkExitCondition:[6,3,1,""]},"src.simulation.simulationrunner.ExitConditionBuilder":{build:[6,3,1,""]},"src.simulation.simulationrunner.MetricExitCondition":{checkExitCondition:[6,3,1,""]},"src.simulation.simulationrunner.PeleSimulation":{createSymbolicLinks:[6,3,1,""],runSimulation:[6,3,1,""]},"src.simulation.simulationrunner.RunnerBuilder":{build:[6,3,1,""]},"src.simulation.simulationrunner.SimulationRunner":{checkExitCondition:[6,3,1,""],hasExitCondition:[6,3,1,""],makeWorkingControlFile:[6,3,1,""],runSimulation:[6,3,1,""]},"src.simulation.simulationrunner.TestSimulation":{makeWorkingControlFile:[6,3,1,""],runSimulation:[6,3,1,""]},"src.spawning":{densitycalculator:[7,0,0,"-"],densitycalculatortypes:[7,0,0,"-"],spawning:[7,0,0,"-"],spawningTypes:[7,0,0,"-"]},"src.spawning.densitycalculator":{ContinuousDensityCalculator:[7,2,1,""],DensityCalculator:[7,2,1,""],DensityCalculatorBuilder:[7,2,1,""],DensityCalculatorHeaviside:[7,2,1,""],NullDensityCalculator:[7,2,1,""]},"src.spawning.densitycalculator.ContinuousDensityCalculator":{calculate:[7,3,1,""]},"src.spawning.densitycalculator.DensityCalculator":{calculate:[7,3,1,""]},"src.spawning.densitycalculator.DensityCalculatorBuilder":{build:[7,3,1,""]},"src.spawning.densitycalculator.DensityCalculatorHeaviside":{calculate:[7,3,1,""]},"src.spawning.densitycalculator.NullDensityCalculator":{calculate:[7,3,1,""]},"src.spawning.densitycalculatortypes":{DENSITY_CALCULATOR_TYPES:[7,2,1,""]},"src.spawning.densitycalculatortypes.DENSITY_CALCULATOR_TYPES":{"null":[7,4,1,""],continuous:[7,4,1,""],heaviside:[7,4,1,""]},"src.spawning.spawning":{DensitySpawningCalculator:[7,2,1,""],EpsilonDegeneracyCalculator:[7,2,1,""],FASTDegeneracyCalculator:[7,2,1,""],IndependentRunsCalculator:[7,2,1,""],InverselyProportionalToPopulationCalculator:[7,2,1,""],SameWeightDegeneracyCalculator:[7,2,1,""],SimulatedAnnealingCalculator:[7,2,1,""],SpawningAlgorithmBuilder:[7,2,1,""],SpawningBuilder:[7,2,1,""],SpawningCalculator:[7,2,1,""],SpawningParams:[7,2,1,""],VariableEpsilonDegeneracyCalculator:[7,2,1,""],return_sign:[7,1,1,""]},"src.spawning.spawning.DensitySpawningCalculator":{calculateDensities:[7,3,1,""]},"src.spawning.spawning.EpsilonDegeneracyCalculator":{calculate:[7,3,1,""],divideProcessorsMetricProportional:[7,3,1,""],log:[7,3,1,""]},"src.spawning.spawning.FASTDegeneracyCalculator":{calculate:[7,3,1,""],calculateNormalisedMetrics:[7,3,1,""],calculateNormalisedSizes:[7,3,1,""],log:[7,3,1,""],normaliseArray:[7,3,1,""]},"src.spawning.spawning.IndependentRunsCalculator":{calculate:[7,3,1,""],log:[7,3,1,""],writeSpawningInitialStructures:[7,3,1,""]},"src.spawning.spawning.InverselyProportionalToPopulationCalculator":{calculate:[7,3,1,""],log:[7,3,1,""]},"src.spawning.spawning.SameWeightDegeneracyCalculator":{calculate:[7,3,1,""],log:[7,3,1,""]},"src.spawning.spawning.SimulatedAnnealingCalculator":{calculate:[7,3,1,""],computeTemperature:[7,3,1,""],log:[7,3,1,""]},"src.spawning.spawning.SpawningAlgorithmBuilder":{build:[7,3,1,""]},"src.spawning.spawning.SpawningBuilder":{buildSpawningCalculator:[7,3,1,""]},"src.spawning.spawning.SpawningCalculator":{calculate:[7,3,1,""],divideInverselyProportionalToArray:[7,3,1,""],divideProportionalToArray:[7,3,1,""],divideTrajAccordingToWeights:[7,3,1,""],getMetrics:[7,3,1,""],getSizes:[7,3,1,""],log:[7,3,1,""],writeSpawningInitialStructures:[7,3,1,""]},"src.spawning.spawning.SpawningParams":{buildSpawningParameters:[7,3,1,""]},"src.spawning.spawning.VariableEpsilonDegeneracyCalculator":{calculate:[7,3,1,""],calculateEpsilonValue:[7,3,1,""],linearVariation:[7,3,1,""],log:[7,3,1,""]},"src.spawning.spawningTypes":{EPSILON_VARIATION_TYPES:[7,2,1,""],SPAWNING_TYPES:[7,2,1,""]},"src.spawning.spawningTypes.EPSILON_VARIATION_TYPES":{linearVariation:[7,4,1,""]},"src.spawning.spawningTypes.SPAWNING_TYPES":{FAST:[7,4,1,""],epsilon:[7,4,1,""],independent:[7,4,1,""],inverselyProportional:[7,4,1,""],sameWeight:[7,4,1,""],simulatedAnnealing:[7,4,1,""],variableEpsilon:[7,4,1,""]},"src.utilities":{clusteringUtilities:[8,0,0,"-"],utilities:[8,0,0,"-"]},"src.utilities.clusteringUtilities":{writeStructures:[8,1,1,""]},"src.utilities.utilities":{assertSymmetriesDict:[8,1,1,""],calculateContactMapEigen:[8,1,1,""],cleanup:[8,1,1,""],getRMSD:[8,1,1,""],getSnapshots:[8,1,1,""],getTrajNum:[8,1,1,""],makeFolder:[8,1,1,""],readClusteringObject:[8,1,1,""]},"src.validator":{controlFileValidator:[9,0,0,"-"]},"src.validator.controlFileValidator":{validate:[9,1,1,""],validateBlock:[9,1,1,""],validateGeneralBlock:[9,1,1,""]},src:{__init__:[0,0,0,"-"],adaptiveSampling:[0,0,0,"-"],automateRoundsAdaptive:[0,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute"},terms:{"abstract":7,"boolean":[1,4,5],"case":[0,1],"class":[4,5,6,7],"default":[1,5],"final":[0,1],"float":[1,4],"function":[1,4,7,8],"int":4,"new":[0,5],"null":[1,7],"return":[0,3,4,5],"true":[1,4,5,8],"try":1,"while":1,accept:1,accord:[1,3,5],accumul:[1,5],adapt:[0,1],addclust:5,addelement:5,addit:5,additionali:1,addsnapshottoclust:5,affect:5,affin:5,after:1,agglom:5,algorithm:[1,5],all:[0,1,3,4,5,6,8],alpha:4,alreadi:1,also:1,altough:1,amstrogm:4,amstrong:4,analys:5,analysi:[],angstrom:4,ani:[0,1,5],arg:0,arrai:[4,5,7],assertsymmetriesdict:8,assign:[1,5,7],atom2:4,atom:[1,4,5],atomcont:4,atomid:4,atomnam:4,atomseri:4,atomset:[],attribut:0,automatesimul:0,avail:1,averag:[1,5],awai:4,back:7,base:[5,6,7],begin:7,behaviour:7,belong:5,below:1,best:1,between:[1,4,5],bind:1,block:[0,1],blocknam:9,bodi:0,boltzmann:1,bool:4,both:1,build:[0,4,5,6,7],buildclust:5,buildclusterspervalu:3,buildcontactmap:4,buildcontactmapwithrowmap:4,buildgnuplotstr:3,buildnewclusteringandwriteinitialstructuresinnewsimul:0,buildnewclusteringandwriteinitialstructuresinrestart:0,buildoptimalpermutationcontactmap:4,buildspawningcalcul:7,buildspawningparamet:7,calcul:[0,1,4,5,7],calculatecontactmapeigen:8,calculatecorrelationcontactmap:4,calculatedens:7,calculateepsilonvalu:7,calculatenormalisedmetr:7,calculatenormaliseds:7,call:[1,4],calul:1,can:[1,5],carbon:4,center:[4,5],centroid:4,certain:[0,1,5],chang:[0,1],check:[0,4,6],checkattribut:5,checker:8,checkexitcondit:6,checksymmetrydict:0,cleancontactmap:5,cleanup:8,click:1,close:1,closer:[1,5],cluster:[],cluster_center_indic:5,cluster_memb:5,clusteragglomerativecontactmap:5,clustercontactmap:[4,5],clusterepochtraj:0,clustering:6,clustering_types:5,clusteringblock:[0,5],clusteringbuild:5,clusteringexitcondit:6,clusteringmethod:0,clusteringobject:8,clusteringobjectpath:8,clusteringoutputobject:0,clusteringparam:7,clusteringresultsparamet:5,clusteringtyp:[],clusteringutil:[],clusterkmean:5,clusternum:5,clusterpreviousepoch:0,clustersperepoch:3,clusterspervalu:3,cmclusteringevalu:5,col:5,column1:3,column2:3,column:[0,1,3,4,5],columnofreportfil:5,compar:4,complet:1,complex:0,comprehens:1,comput:4,computecomdiffer:4,computecomsquareddiffer:4,computenonsymmatom:4,computermsd2:4,computermsd:4,computesquaredcentroiddiffer:4,computetemperatur:7,computetotalmass:4,condit:[1,5,7],condtion:6,configur:1,conform:[1,4],connect:5,consid:[1,3,4,5],constant:[0,1,5,7],conta:0,contact:[1,4,5,7],contactmap:[1,4,5,8],contactmapaccumul:5,contactmapaccumulativeclust:5,contactmapaffin:5,contactmapagglom:5,contactmapagglomerativeclust:5,contactmapclust:5,contactmapnew:[],contactsclust:5,contactsclusteringevalu:5,contactthresholddist:[1,4,5],contacttreshold:1,contain:[0,1,4,5,7],contanct:4,content:[2,4],continu:[1,7],continuousdensitycalcul:7,control_fil:9,controlfil:[0,1,3],controlfileblock:9,controlfilevalid:[],coordin:4,copi:0,copyinitialstructur:0,correct:[0,1],correctrmsd:[],correl:[1,4,5],correlationevalu:5,correspond:4,count:[4,5],countcontact:4,creat:[0,1,4,5,7],createcontactmap:4,createmultiplecomplexesfilenam:0,createsymboliclink:6,current:[0,1,3],currentepoch:[0,7],data:1,debug:[0,1],decid:5,defin:5,definit:7,degeneraci:[5,7],degeneracyofrepres:7,delet:0,densiti:[1,5,7],density_calculator_types:7,densitycalcul:[],densitycalculatorbuild:7,densitycalculatorheavisid:7,densitycalculatortyp:[],densityspawningcalcul:7,depend:7,determin:5,develop:5,diagram:1,dict:1,dictionari:[0,3,4,6],dictonari:0,differ:[1,3,4,5,7],differencedist:5,differencedistanceevalu:5,discret:1,distanc:[1,4,5],distribut:1,divid:7,divideinverselyproportionaltoarrai:7,divideprocessorsmetricproport:7,divideproportionaltoarrai:7,dividetrajaccordingtoweight:7,document:[],doe:1,doubl:5,each:[1,5,7],earli:5,element:[1,3,5],end:1,energi:7,enough:[1,5],ensur:7,entri:1,epoch:[0,3,5,7],epochoutputpathtemplet:0,epsilon:[1,7],epsilon_variation_types:7,epsilondegeneracycalcul:7,equal:[3,7],evalu:[1,8],evaluat:5,evaluatecorrel:4,evaluatedifferencedist:4,evaluatejaccard:4,everi:1,exampl:1,except:1,execut:1,exempl:1,exemplar:5,exit:[1,6],exitcondit:1,exitcondition_type:6,exitconditionblock:6,exitconditionbuild:6,exitvalu:1,explor:7,extendreportwithrmsd:3,extract:[0,5],extractcentroid:4,extractcom:4,fals:[1,3,4,5,8],fast:7,fastdegeneracycalcul:7,field:1,filenam:[0,8],finalepoch:0,find:[0,5],finddifferentclustersforallepoch:3,finddifferentclustersinepoch:3,findfirstrun:0,fine:1,first:[0,1,4,5],firstrun:0,five:1,fixedreport_i:0,fixreportssymmetri:0,flow:1,folder:[1,3,5],foldersfirstbindingev:[],follow:1,followin:[],foo:[],format:[0,4],found:[3,5],four:1,fourth:1,fraction:1,from:[0,4,5],futur:1,generateforloopstr:3,generategnuplotfil:[],generatenestedstr:3,generateprintstr:3,generatesnapshotselectionstringlastround:0,get:[1,4],getalldifferentvalu:3,getalltrajectori:5,getatom:4,getatomcoord:4,getcentroid:4,getclust:5,getclusteringsummarycont:3,getcom:4,getcontact:5,getinnerlimit:5,getmaxthreshold:5,getmetr:[5,7],getmetricfromcolumn:5,getnumberclust:5,getnumberofatom:4,getnumberofclustersperepochforgivencolumn:3,getrmsd:8,getsiz:7,getsnapshot:8,gettotalnumberofclustersperepoch:3,gettrajnum:8,getworkingclusteringobject:0,give:1,given:0,gnuplotstr:3,greater:1,gropu:4,group:1,hasexitcondit:6,have:[0,1,4,5],heavi:[1,4,5],heavisid:[1,5,7],heavyatom:4,helper:[4,5,7],hetero:4,hierarch:5,hold:0,how:1,ignor:5,imag:1,implement:1,includ:[0,1],independ:7,independentrunscalcul:7,index:[1,2,5],indic:[4,5],info:4,inform:[0,4,5],inherit:5,initi:[0,7],initialis:4,initialstructur:[0,1],initialstructuresasstr:0,input:[0,5],insert:5,insertclust:5,instanc:7,instead:1,integ:1,interest:[1,5],intersect:5,interst:8,intial:1,invers:[1,7],inverselyproport:[1,7],inverselyproportionaltopopulationcalcul:7,iselement:5,isheavyatom:4,isheteroatom:4,isprotein:4,issimilarclust:5,iter:[0,1,7],iterat:6,iteri:7,jaccard:[1,5],jaccardevalu:5,json:[0,1],jsonparam:0,kei:1,keyerror:4,kindofprint:3,kmean:5,know:0,label:5,lambda:8,larger:1,last:[0,1,5,7],lastsnapshot:5,length:3,less:[1,4],letter:5,ligan:5,ligand:[0,1,4,5],ligandatom:5,ligandresnam:[1,4],like:1,line:4,linear:[1,7],linearvari:7,list:[0,1,3,4,5],liststructur:8,load:4,loadparam:0,log:7,look:1,mai:4,main:[0,3],makefold:8,makepng:[],makeworkingcontrolfil:6,mandatori:1,mani:4,map:[1,4,5],mass:4,matric:1,matrix:[1,4],maxepsilon:1,maxepsilonwindow:1,maxim:4,maximum:[1,4,5],mean:1,meanwhil:1,member:5,met:6,method:[0,1,4,5],metric:[1,5,6],metriccol:[1,5,6],metriccolumninreport:1,metricexitcondit:6,metrics_weight:5,metricvalu:6,metricweight:[1,7],might:1,minepsilon:1,minimum:[1,5],mode:1,modifi:1,moment:1,more:1,much:1,multipl:5,must:[5,7],n_cluster:5,name:[0,1,4,5],nativ:[0,1],nativepdb:8,nativestructur:[0,1],ncluster:5,need:[0,1],needtoreclust:0,newclusteringmethod:0,next:[1,7],none:[5,7],normal:7,normalisearrai:7,ntraj:6,nulldensitycalcul:7,number:[0,1,3,4,5,7],numberofepoch:3,numberofownclust:[],numberofsnapshot:0,numcol:5,numpi:[4,5],numtraj:7,object:[0,4,5,7,8],obtain:[1,5],old:5,oldclusteringmethod:0,onl:4,onli:[1,3,4,5],only:5,option:1,optional:1,order:5,originalcontrolfil:0,other:1,otherwis:[4,5],output:[0,5,7,8],outputdir:8,outputfilenam:3,outputobject:5,outputpath:[0,1,5,8],outputpathconst:[0,7],outsid:1,over:[1,5,6],page:[1,2],paht:5,paramet:[0,1,4,5,6],pars:4,parsearg:[0,3],parseargu:[0,3],pass:5,path:[0,1,4,5,7],pdb1:4,pdb2:4,pdb:[0,1,4,5,8],pdb_list:5,pdbfile:4,pdbobj:4,pdbstr:4,pele:[0,1,5,6,7],pelecontrolfiledictionari:0,pelesimul:6,pelestep:1,perio:1,period:1,permut:4,pickl:5,piec:7,plan:1,plotclusterspervalu:3,plotcontactshistogram:3,point:1,popul:[1,7],possibl:5,prefer:5,preparepelecontrolfil:0,previou:[0,1,3,5],print:[4,8],printatom:4,printclust:5,printhelp:3,printwithlin:3,process:[1,5],processclusterresult:5,processor:[1,7],processsnapshot:5,program:[0,1],propag:[1,5],properli:0,proport:[1,7],proportion:7,protein:[1,4,5],provid:[0,5],purpos:7,rais:4,random:1,randomli:5,ratio:[1,5],ration:1,reach:1,read:0,readclusteringobject:8,readcontrolfil:3,readpdb:4,real:1,receptor:1,reclust:0,redo:0,refer:1,region:1,relat:[0,4],replotfirst:3,report:[0,1,5],reportbasefilenam:5,reportfil:[0,3],reportfilenam:1,reportnam:3,repres:[1,5],requir:5,residu:[0,1,4],resnam:[0,4,5,8],rest:[1,7],restart:[0,1],result:[1,5],return_sign:7,rmsd:[0,1,3,4],rmsdcalcul:[4,5],row:[1,4],run:[0,1,5],runner:0,runnerbuild:6,runningcontrolfil:6,runsimul:6,same:[1,5],sameweight:[1,7],sameweightdegeneracycalcul:7,sampl:[],save:0,saveinitialcontrolfil:0,screenshot:1,search:2,second:[1,4,5],section:1,see:[1,5],seed:1,select:[1,4],selectrandomcent:5,self:5,separ:1,sequenti:[3,5],sequentiallastsnapshotclust:5,seri:5,set:[1,3],setcol:5,sever:1,should:[1,5,8],show:1,shown:1,similar:[1,4,5],similarity_types:5,similarityevalu:[1,5],similarityevaluatorbuild:5,similarityevaluatortyp:5,similariyevalu:5,similarli:1,simpl:1,simul:[],simulatedann:7,simulatedannealingcalcul:7,simulation_type:6,simulationparamet:6,simulationrunn:[],simulationrunnerblock:6,simulationtyp:[],site:1,size:1,smaller:1,snapshot:5,snaptshot:5,sometim:5,sourc:[0,3,4,5,6,7,8,9],spawn:[],spawning_types:7,spawningalgorithmbuild:7,spawningblock:7,spawningbuild:7,spawningcalcul:[0,7],spawningparam:[0,7],spawningtyp:[],specif:1,specifi:[0,1,5],split:7,squar:4,squareddist:4,src:[0,3,4,5,6,7,8,9],stand:5,start:1,step:[1,3,7],stepsperepoch:3,stepsperrun:3,store:0,str:[4,5],strategi:[1,7],string:[0,1,4,5],structur:[0,1,5,7,8],strutctur:0,subclass:7,subset:1,substitut:0,sum:7,summar:1,summari:[3,5],summaryfil:3,symcontactmapevalu:5,symmetr:[1,4],symmetri:[0,1,4,5,8],symmetricalatomid:4,symmetrycontactmapevalu:4,symmetryevalu:5,system:0,taht:5,take:1,temperatur:1,templat:0,templet:[0,1],templetizedclusteringsummaryfil:3,termin:1,test:[1,6],testsimul:6,than:[1,4,5],thei:1,them:1,therefor:1,thi:[1,3,5,7],thir:[],those:1,three:[1,5,7],threhold:[],threshold:[1,3,5],threshold_calculator_types:5,thresholdcalcul:[],thresholdcalculatorbuild:5,thresholdcalculatorconst:5,thresholdcalculatorheavisid:5,thresholdcalculatortyp:[],thresholdradiu:5,time:1,titl:3,tmpfolder:8,tmpinitialstructurestempl:0,togeth:5,total:4,totalnumberofstep:3,traj:8,trajecotori:0,trajectori:[0,1,5,7],trajectoryfil:8,trajfilenam:8,trajtodistribut:7,trajtodivid:7,treshold:[1,5],two:[1,4,5],txt:3,type:[1,4],typic:1,uncheck:6,uniformli:1,union:5,until:0,usual:1,util:[],valid:[],validateblock:9,validategeneralblock:9,valu:[0,1,3,4,5,7],valueerror:4,varepsilontyp:1,variableepsilon:[1,7],variableepsilondegeneracycalcul:7,variat:1,variationwindow:1,verbos:[5,8],version:[1,4],wai:7,want:1,weight:[1,5,7],weigth:1,wether:[1,4,5],what:0,where:[0,1,4,5],whether:0,which:[1,4,7],whom:4,wich:[4,5],wikipedia:1,without:1,work:0,workingcontrolfilenam:6,would:1,write:[0,1,4,5,7],writeal:5,writeallclusteringstructur:1,writeclusteringstructur:[],writeoutput:5,writepdb:[4,5],writespawninginitialstructur:7,writestructur:8,written:1,xcol:3,ycol:3,you:1,zero:1},titles:["AdaptiveSampling Package","Adaptive Sampling Overview","Welcome to AdaptiveSampling&#8217;s documentation!","analysis Package","atomset Package","clustering Package","simulation Package","spawning Package","utilities Package","validator Package"],titleterms:{adaptiv:1,adaptivesampl:[0,2],analysi:3,atomset:4,automateroundsadapt:0,cluster:[1,5],clusteringtyp:5,clusteringutil:8,control:[],controlfilevalid:9,correctrmsd:3,densitycalcul:7,densitycalculatortyp:7,document:2,file:[],foldersfirstbindingev:3,gener:1,generategnuplotfil:3,indice:2,makepng:3,modul:[0,3,4,5,6,7,8,9],numberofownclust:3,overview:1,packag:[0,3,4,5,6,7,8,9],param:1,sampl:1,simul:[1,6],simulationrunn:6,simulationtyp:6,spawn:[1,7],spawningtyp:7,subpackag:0,tabl:2,thresholdcalcul:5,thresholdcalculatortyp:5,util:8,valid:9,welcom:2,writeclusteringstructur:3}})