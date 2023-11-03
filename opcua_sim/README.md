# Idee
- 

# Da implementare

## Clean code
- [ ] usare questa funzione .read_data_type_as_variant_type() per leggere e inserire il data type in un struct
traimite le costanti di opcua_constant.py
- [ ] come gestire diverse meglio la classe opcua_constant magari con un design pattern
- [ ] aggiungere attributi di funzione ricorsiva alla funzione create_server_structure()
    in server.py in modo da non doverli passare ogni volta
- [ ] non importare direttamente Node e Server (in genere non importare direttamente cose) 
    dalla libraria asyncua 

## test stack
- [ ] osservare struttura di un opc reale 
- [ ] testare copia di un opc reale 

## BUG
- [ ] importare opcua_constant

## Fondamentali
- [ ] creare libreria per scriptre funzioni
- [ ] il server deve cercare il suo ip ne file server_struct.json
- [ ] docker compose per creare piu docker
- [X] client che scannerizza piu server per salvare piu strutture alla volta

## Serviranno
- [ ] poter scegliere tra un import tramite xml (nativo) o una scansione dei nodi nel 
    caso l'import nativo abbia qualche problema

## In un futuro molto lontano
- [ ] formatter tutti i file seguendo uno standard
- [ ] asincornismo nella ricerca ad albero in modo da velocizzare

### COSE

