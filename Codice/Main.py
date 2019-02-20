from copy import deepcopy
from matplotlib.pyplot import *

from HeuristicSearch import *
from Search import astar_search
from Utils import calculateEffectiveBranchingFactor

start = timer()

# grandezza lato della matrice
n = 3

# variabili per controllare l'esecuzione dell'esperimento
nScrambles = 50 # numero massimo di scambi
numTests = 10 # numero di test

# inizializzo variabili per calcolo prestazioni algoritmi
avgnumExpandedNodesM = 0
avgeffectiveBranchingFactorM = 0
avgpenetranceM = 0

avgnumExpandedNodesPDB = 0
avgeffectiveBranchingFactorPDB = 0
avgpenetrancePDB = 0

for i in range(numTests):
    # creo un problema
    puzzleProblemM = Puzzle(n, nScrambles)
    # copio il problema
    puzzleProblemPDB = deepcopy(puzzleProblemM)

    ''' Manhattan heuristic '''
    nodeResultM, numExpandedNodesM = astar_search(puzzleProblemM, h_manhattan)
    avgnumExpandedNodesM += numExpandedNodesM

    effectiveBranchingFactorM = calculateEffectiveBranchingFactor(numExpandedNodesM, nodeResultM.path_cost)
    avgeffectiveBranchingFactorM += effectiveBranchingFactorM

    penetranceM = float(nodeResultM.path_cost) / numExpandedNodesM
    avgpenetranceM += penetranceM

    ''' Pattern databases heuristic '''
    nodeResultPDB, numExpandedNodesPDB = astar_search(puzzleProblemPDB, h_dbPattern)
    avgnumExpandedNodesPDB += numExpandedNodesPDB

    penetrancePDB = float(nodeResultPDB.path_cost) / numExpandedNodesPDB
    avgpenetrancePDB += penetrancePDB

    effectiveBranchingFactorPDB = calculateEffectiveBranchingFactor(numExpandedNodesPDB, nodeResultPDB.path_cost)
    avgeffectiveBranchingFactorPDB += effectiveBranchingFactorPDB

# divido variabili per numero di test effettuati
avgnumExpandedNodesM /= float(numTests)
avgeffectiveBranchingFactorM /= numTests
avgpenetranceM /= numTests

avgnumExpandedNodesPDB /= float(numTests)
avgpenetrancePDB /= numTests
avgeffectiveBranchingFactorPDB /= numTests

end = timer()
print end - start

print

print "Manhattan heuristic"

print "Average number of expanded nodes: ", avgnumExpandedNodesM
print "Average effective branching factor: ", avgeffectiveBranchingFactorM
print "Average penetrance: ", avgpenetranceM
#printSolution(nodeResultM)

print

print "Pattern databases heuristic"

print "Average number of expanded nodes: ", avgnumExpandedNodesPDB
print "Average effective branching factor: ", avgeffectiveBranchingFactorPDB
print "Average penetrance: ", avgpenetrancePDB
#printSolution(nodeResultPDB)


''' grafici '''
x = [0, 1]
xLabel = ["manhattan", "pattern databases"]

# primo grafico: numero nodi espansi
y = [avgnumExpandedNodesM, avgnumExpandedNodesPDB]
figure(1)
bar(x, y, width=0.4, tick_label=xLabel)
xticks(size=20)
yticks(size=10)
suptitle("Average number of expanded nodes", size=19)
title("(lower is better)", size=14)
ylabel("number of expanded nodes", size=20)
show()

# secondo grafico: effective branching factor
y = [avgeffectiveBranchingFactorM, avgeffectiveBranchingFactorPDB]
figure(2)
bar(x, y, width=0.4, tick_label=xLabel)
xticks(size=20)
yticks(size=10)
suptitle("Average Effective Branching Factor", size=19)
title("(lower is better)", size=14)
ylabel("effective branching factor", size=20)
show()

# terzo grafico: penetranza
y = [avgpenetranceM, avgpenetrancePDB]
figure(3)
bar(x, y, width=0.4, tick_label=xLabel)
xticks(size=20)
yticks(size=10)
suptitle("Average penetrance", size=19)
title("(higher is better)", size=14)
ylabel("penetrance", size=20)
show()