# Eight Puzzle
## Funzionamento in sintesi
Nel programma, partendo da un'implementazione dell'algoritmo A\*, si vuole implementare la strategia di generazione di euristiche ammissibili e analizzare sperimentalmente A\* realizzata con l'euristica basata sulla distanza Manhattan con A\* basata sui database pattern in termini di numero di nodi espansi, penetranza e branching factor. 

## Utilizzo del programma
Per eseguire l'esperimento i passi sono i seguenti:

1. *Opzionale*: Modificare i parametri relativi alla creazione dei dizionari, che si trovano all'inizio del file HeuristicSearch.py

2. Creare i dizionari eseguendo il file HeuristicSearch.py, oppure usare quelli forniti. Nel caso si scelga la prima opzione, il tempo di creazione totale è di circa 1 ora.

3. *Opzionale*: Modificare parametri relativi all'esecuzione dei test, che si trovano all'inizio del file Main.py. 

4. Eseguire il file Main.py. Se si vuole eseguire un nuovo esperimento, è possibile cambiare i parametri relativi ad esso senza dover creare nuovamente i dizionari.

## Parametri
I parametri che regolano il funzionamento del programma sono di due tipologie: alcuni relativi alla creazione dei file con i costi dei sotto-problemi, altri relativi all'esecuzione dei test.

Si riportano di seguito i parametri con la relativa spiegazione.

Parametri relativi alla creazione dei file, uno dei seguenti per ogni sotto-problema:

+ relevantNumbers: lista delle caselle prese in considerazione nel sotto-problema;

+ dbPattern: file sul quale salvare i costi delle varie istanze del sotto-problema.

Parametri relativi all'esecuzione dei test:

+ nScrambles: numero massimo di scambi che possono essere fatti a partire dalla stato obbiettivo e al termine dei quali si ottiene lo stato iniziale da cui partono i processi di ricerca;

+ numTests: numero di test da eseguire.

