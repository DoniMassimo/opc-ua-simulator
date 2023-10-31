# Idee
- 

# Da implementare

## Clean code
- [ ] usare questa funzione .read_data_type_as_variant_type() per leggere e inserire il data type in un struct
- [X] get_node_attr() in client.py deve ritornare un dizionario per semplificare l'accesso dei 
traimite le costanti di opcua_constant.py
- [ ] come gestire diverse meglio la classe opcua_constant magari con un design pattern
- [ ] aggiungere attributi di funzione ricorsiva alla funzione create_server_structure()
    in server.py in modo da non doverli passare ogni volta
- [ ] non importare direttamente Node e Server (in genere non importare direttamente cose) 
    dalla libraria asyncua 

## test stack
- [X] vedere se usando xmlexporte di asyncua se creano gli attributi dei nodi in modo piu consistente
    - si puo fare ma e' instabile
- [ ] osservare struttura di un opc reale 
- [X] verificare collegamento ignition con semplice server
- [ ] testare copia di un opc reale 

## Fondamentali
- [X] fare in modo che nel file struct vengano inseriti anche index diversi da ns=n;n=n 
- [X] mettere tutti i ;e variabile in write mode
- [X] cegliere se inserire il valore corrente on mettere il default quando vengono generatew le variabili del server
- [X] trasformare la struttura opc in un file
- [X] generare un server da una struttura di un file 


## Serviranno
- [ ] riuscire a simulare diversi ip sullo stesso pc
- [ ] poter scegliere tra un import tramite xml (nativo) o una scansione dei nodi nel 
    caso l'import nativo abbia qualche problema

## In un futuro molto lontano
- [ ] formatter tutti i file seguendo uno standard
- [ ] asincornismo nella ricerca ad albero in modo da velocizzare

### COSE
 
