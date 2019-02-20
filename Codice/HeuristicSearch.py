import pickle
from EightPuzzle import Puzzle, PuzzleState, matrixToString, Problem
import itertools
from timeit import default_timer as timer
from Search import best_first_graph_search

# sottoinsiemi delle caselle prese in considerazione nei vari sotto-problemi
# 0 indica la casella vuota, e' necessario che faccia parte del sottoinsieme
relevantNumbers1 = [0,1,2,3,4]
relevantNumbers2 = [0,5,6,7,8]

# file nei quali vengono salvati i costi delle varie istanze di un sotto-problema
dbPattern1 = "dbPattern_01234.p"
dbPattern2 = "dbPattern_05678.p"

# classe che definisce il sotto-problema del puzzle
class SubPuzzle(Puzzle):
    def __init__(self, N, relevantNumbers, initial=None, goal=None):
        # chiamo costruttore classe padre
        Puzzle.__init__(self, N, 0, initial, goal)

        # al posto delle caselle che non fanno parte del sotto-problema metto il valore -1
        self.relevantNumbers = relevantNumbers
        for i in range(N * N):
            if self.initial.matrix[i] not in relevantNumbers:
                self.initial.matrix[i] = -1

    # ridefinisco path_cost in modo da rendere i database pattern disgiunti
    def path_cost(self, c, state1, action, state2):
        # per vedere con quale valore effettuo lo scambio, guardo il valore in state1 alle coordinate
        # della casella vuota in state2
        i = state2.row
        j = state2.column
        valueSwapped = state1.matrix[i * state1.N + j]
        # non voglio contare gli scambi dei numeri che non ci interessano (ovvero quelli con il valore -1)
        if valueSwapped != -1:
            # calcolo costo normalmente
            return Problem.path_cost(self, c, state1, action, state2)
        else:
            # calcolo costo senza contare scambio
            return c

    # ridefinisco goal_test in modo da non considerare le caselle che non fanno parte del sotto-problema
    def goal_test(self, state):
        N = state.N
        stateMatrix = state.matrix
        goalMatrix = self.goal.matrix
        for i in range(N*N):
            if stateMatrix[i] != -1:
                # se la casella fa parte del sotto-problema
                if stateMatrix[i] != goalMatrix[i]:
                    # se la casella e' nella posizione sbagliata
                    return False
        return True


# usando solo questa funzione per l'algoritmo best_first_graph_search
# si realizza la uniform cost
def g(node):
    return node.path_cost


# usando questa funzione per l'algoritmo best_first_graph_search
# si realizza A* con euristica di distanza Manhattan
def f_manhattan(node):
    return g(node) + h_manhattan(node)

# euristica di distanza Manhattan
def h_manhattan(node):
    n = node.state.N
    matrix = node.state.matrix
    distanza = 0
    for i in range(n):
        for j in range(n):
            if matrix[i*n + j] == -1:
                continue
            ig = matrix[i*n + j] / n    # riga goal per l'elemento ij
            jg = matrix[i*n + j] % n    # colonna goal per l'elemento ij
            costo_ij = abs(ig - i) + abs(jg - j)
            distanza = distanza + costo_ij
    return distanza


# usando questa funzione per l'algoritmo best_first_graph_search
# si realizza A* con euristica database di pattern
def f_dbPattern(node):
    return g(node) + h_dbPattern(node)


# euristica calcolata con database di pattern disgiunti
def h_dbPattern(node):
    h1 = h_dbPattern_aux(node, relevantNumbers1, dict1)
    h2 = h_dbPattern_aux(node, relevantNumbers2, dict2)
    return h1 + h2


# legge il valore dell'euristica per uno dei sotto-problemi all'interno del dizionario
def h_dbPattern_aux(node, relevantNumbers, dictionary):
    # copiare matrice
    matrix = node.state.matrix[:]

    # mettere -1 nella copia dove ci sono numeri non rilevanti
    N = node.state.N
    for i in range(N * N):
        if matrix[i] not in relevantNumbers:
            matrix[i] = -1

    # calcolo stringa
    strMatrix = matrixToString(matrix, N)

    # guardo e ritorno corrispondente
    return dictionary[strMatrix]


# calcola l'euristica di ogni istanza di un sotto-problema, memorizzando i costi in un dizionario che viene salvato su file
def createDictionary(N, relevantNumbers, dictionaryFileName):
    dictionary = {}
    matrix = range(N*N)
    start = timer()
    for i in range(N*N):
        if matrix[i] not in relevantNumbers:
            matrix[i] = -1
    # matrix adesso contiene lo stato goal, dove i numeri non rilevanti sono stati sostituiti con "-1"

    # genero tutte le possibili permutazioni di matrix
    # uso il set per rimuovere le permutazioni doppioni
    statePermutations = set(itertools.permutations(matrix))

    t1 = 0
    t2 = 0
    # per ogni permutazione
    for matSet in statePermutations:
        # matSet e' una permutazione di matrix, ma rappresentata come set...
        start = timer()
        # ...quindi la trasformo in lista
        mat = list(matSet)
        # creo lo stato iniziale che rappresenta questa permutazione
        initial = PuzzleState(N, matrix=mat)
        # creo il sottoproblema che ha come stato iniziale quello appena creato
        sp = SubPuzzle(N, relevantNumbers, initial=initial)
        end = timer()
        t1 += (end-start)

        start = timer()
        # eseguo la ricerca A*
        nodeResult, numExpandedNodes = best_first_graph_search(sp, f_manhattan)
        # nel dizionario, associo allo stato iniziale il costo della soluzione del sottoproblema appena risolto
        dictionary[initial.__str__()] = nodeResult.path_cost
        end = timer()
        t2 += (end-start)

    # salvo tutto il dizionario sul file, usando la libreria pickle
    pickle.dump(dictionary, open(dictionaryFileName, "wb"))

    print "time 1: ", t1
    print "time 2: ", t2


start = timer()

if __name__ == "__main__":
    # i dizionari vengono creati soltanto quando viene eseguito questo file, e non quando viene importato
    createDictionary(3, relevantNumbers1, dbPattern1)
    createDictionary(3, relevantNumbers2, dbPattern2)

# carico dizionari
dict1 = pickle.load(open(dbPattern1, "rb"))
dict2 = pickle.load(open(dbPattern2, "rb"))

end = timer()

if __name__ == "__main__":
    print "tempo: ", (end-start)