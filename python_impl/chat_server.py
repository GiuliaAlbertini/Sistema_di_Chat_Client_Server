#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#dizionario registrazione dei client in ingresso e nomi associati agli indirizzi
clients = {}
indirizzi = {}

#funzione che accetta le connessioni dei client in entrata
def accetta_connessioni_in_entrata():
    while True:
        try:
            #restituisco un nuovo socket client e l'indirizzo del client
            client, client_address = SERVER.accept()
            print("%s:%s si è collegato." % client_address)
            #messsaggio di benvenuto codificato in UTF-8
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            #utilizzo il registro indirizzi per registrare il client
            indirizzi[client] = client_address
            #creo il thread per gestire la comunicazione con il client - uno per ciascun client
            Thread(target=gestisce_client, args=(client,client_address)).start()
        except Exception as e:
            print(f"Errore nella connessione con {client_address}: {e}\n")
            break
        

 #funzione che gestisce la connessione di un singolo client
def gestisce_client(client,client_address):  #Prendo il socket del client come argomento della 
    #salvo nella varibile "nome" i dati inviati dal client
    print("Connessione stabilita")
    nome = client.recv(BUFSIZ).decode("utf8")
    #benvenuto al client e indicazioni per uscire dalla chat quando ha terminato
    benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % nome
    client.send(bytes(benvenuto, "utf8"))
    #messaggio che notifica a tutti i client connessi che l'utente x è entrato
    msg = "%s si è unito alla chat!" % nome
    broadcast(bytes(msg, "utf8"))
    #aggiorna il dizionario clients per registrare il nuovo client.
    clients[client] = nome


        
#si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
      try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                client.close()
                del clients[client]
                broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
                print("%s:%s si è disconnesso." % client_address)
                break
            else:
                broadcast(msg, nome+": ")
      except Exception as e:
            print(f"Errore durante la gestione del client %s: {e}" % nome)
            
            
          


# funzione che invia un messaggio in broadcast ai client
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        try:
            utente.send(bytes(prefisso, "utf8") + msg)
        except Exception as e: 
            print(f"Errore durante l'invio del messaggio: {e}\n")
            


#porta e interfaccia server
HOST = ''
PORT = 5000
BUFSIZ = 1024 #dimensione buffer 
ADDR = (HOST, PORT)

#creo il socket TCP
SERVER = socket(AF_INET, SOCK_STREAM)
#associo il socket all'indirizzo di porta specificati
SERVER.bind(ADDR)

if __name__ == "__main__":
    #metto il server in ascolto per le connessioni in entrata (fino a 5 connessioni in entrata)
    SERVER.listen(5)
    print("In attesa di connessioni...")
    #creo il thread che permette al serAver di accettare le connessioni
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    #avvio il thread
    ACCEPT_THREAD.start()
    #attendo la terminazione del thread
    ACCEPT_THREAD.join()
    #chiusura socket
    SERVER.close() 