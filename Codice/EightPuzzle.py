from copy import deepcopy
from Search import *
from random import randint

# la classe rappresenta lo stato del puzzle ovvero la disposizione delle caselle
class PuzzleState:

    # costruttore
    def __init__(self, N, maxMoves=0, matrix=None):
        self.N = N
        if matrix is None:
            # imposto matrix allo stato goal
            self.matrix = range(N*N)
            # imposto posizione casella vuota
            self.row = 0
            self.column = 0
        else:
            # imposto matrix alla matrice che e' stata passata come parametro
            self.matrix = matrix
            # cerco e imposto posizione casella vuota
            for i in range(N):
                for j in range(N):
                    if matrix[i*N + j] == 0:
                        self.row = i
                        self.column = j
                        break

        # faccio delle mosse per disordinare la matrice
        numMoves = 0
        # creo un dizionario per tener traccia degli stati gia' visti
        exploredStates = {}
        while numMoves < maxMoves:
            actions = ['right', 'left', 'up', 'down']
            # elimino le azioni non valide
            if self.row == 0:
                actions.remove('up')
            elif self.row == self.N - 1:
                actions.remove('down')
            if self.column == 0:
                actions.remove('left')
            elif self.column == self.N - 1:
                actions.remove('right')
            # ora scelgo una tra le azioni valide
            actionIndex = randint(0, len(actions) - 1)
            action = actions[actionIndex]
            newState = self.move(action)
            # se lo stato nuovo non e' stato esplorato oppure se non e' possbile raggiungere stati inesplorati
            if (not exploredStates.has_key(newState.__str__())) or self.allExplored(actions, exploredStates):
                # segno lo stato newState come esplorato
                exploredStates[newState.__str__()] = True
                numMoves = numMoves + 1
                # eseguo il passaggio di stato
                self.matrix = newState.matrix
                self.row = newState.row
                self.column = newState.column

    # funzione per controllare se tutti gli stati raggiungibili da quello corrente sono stati esplorati
    # in caso affermativo si permette di tornare in uno stato gia' esplorato
    # utile per evitare che il costruttore non giunga al termine
    def allExplored(self, actions, exploredStates):
        for action in actions:
            newState = self.move(action)
            if not exploredStates.has_key(newState.__str__()):
                return False
        return True

    def __str__(self):
        return matrixToString(self.matrix, self.N)

    def __repr__(self):
        return self.__str__()

    # funzione che scambia due valori della matrice
    def swap(self, row1, column1, row2, column2):
        aux = self.matrix[row1*self.N + column1]
        self.matrix[row1 * self.N + column1] = self.matrix[row2*self.N + column2]
        self.matrix[row2 * self.N + column2] = aux

    # funzione per muovere il tassello bianco (ovvero lo 0)
    def move(self, direction):
        copy = deepcopy(self)
        if direction == 'right' and copy.column != copy.N - 1:
            copy.swap(copy.row, copy.column, copy.row, copy.column + 1)
            copy.column = copy.column + 1
        elif direction == 'left' and copy.column != 0:
            copy.swap(copy.row, copy.column, copy.row, copy.column - 1)
            copy.column = copy.column - 1
        elif direction == 'up' and copy.row != 0:
            copy.swap(copy.row, copy.column, copy.row - 1, copy.column)
            copy.row = copy.row - 1
        elif direction == 'down' and copy.row != copy.N - 1:
            copy.swap(copy.row, copy.column, copy.row + 1, copy.column)
            copy.row = copy.row + 1
        else:
            return None
        return copy


# classe che definisce il problema del puzzle
class Puzzle(Problem):
    def __init__(self, N, maxMoves, initial = None, goal = None):
        if initial is None:
            # crea uno stato iniziale casuale
            initial = PuzzleState(N, maxMoves)
        if goal is None:
            goal = PuzzleState(N, 0)
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        actions = ['right', 'left', 'up', 'down']
        # elimino le azioni non valide
        if state.row == 0:
            actions.remove('up')
        elif state.row == state.N - 1:
            actions.remove('down')
        if state.column == 0:
            actions.remove('left')
        elif state.column == state.N - 1:
            actions.remove('right')

         # ciclo per esplorare tutti i nuovi stati raggiungibili
        for action in actions:
            newState = state.move(action)
            yield (action, newState)

    def goal_test(self, state):
        return state.matrix == self.goal.matrix

# funzione per trasformare la matrice in rappresentazione stringa
def matrixToString(matrix, N):
    # stringa vuota
    s = ""
    # ciclo per creare la stringa che rappresenta il contenuto della matrice
    for i in range(N):
        for j in range(N):
            s = s + str(matrix[i * N + j])
            if j != N - 1:
                s = s + "-"
        if i != N - 1:
            s = s + "\n"  # per visualizzare il puzzle bellino (con \n vado a capo)

    return s





