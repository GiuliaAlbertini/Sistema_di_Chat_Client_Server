#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

#funzione che gestisce la ricezione dei messaggi
def receive():
    while True:
        try:
            #la funzione receive, si mette in ascolto dei messaggi che arrivano sul socket
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #visione elenco dei messaggi sullo schermo (cursore visibile al termine)
            msg_list.insert(tkt.END, msg)
            # in caso di eccezione è probabile che il client abbia abbandonato la chat.
        except OSError:
            break
        
       
#funzione che gestisce l'invio dei messaggi
# gli eventi vengono passati dai binders di tkinter 
# (es. quando si preme il tasto invio)
def send(event=None):
    msg = my_msg.get()  #recupera il messaggio inserito dall'utente dal campo di input
    my_msg.set("") #libera la casella di input
    client_socket.send(bytes(msg, "utf8")) #invia il messaggio al server sul socket
    if msg == "{quit}":
       try:
           client_socket.close()
           finestra.destroy()  # Assicura che il programma si chiuda
       except Exception as e:
           print(f"Errore durante la chiusura del client: {e}")
        

def clear_entry(event):
    entry_field.delete(0, tkt.END)

#----GUI----
finestra = tkt.Tk()
finestra.title("Chat_Client-Server")

#creiamo il frame che contiene i messaggi
chat_frame = tkt.Frame(finestra)
#creiamo una variabile di tipo stringa per i messaggi da inviare.
my_msg = tkt.StringVar()
#indichiamo allo user dove deve scrivere i suoi messaggi
my_msg.set("Scrivi qui i tuoi messaggi.")
#scrollbar per visualizzare i messaggi precedenti.
scrollbar = tkt.Scrollbar(chat_frame)


#messaggi
msg_list = tkt.Listbox(chat_frame, height=20, width=60, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.LEFT, fill=tkt.Y)
msg_list.pack(side=tkt.RIGHT, fill=tkt.BOTH)
msg_list.pack()
chat_frame.pack()

#campo di input associato alla variabile stringa
entry_field = tkt.Entry(finestra, textvariable=my_msg)
#lego la funzione send al tasto Return
entry_field.bind("<Return>", send)

#evento  focus per pulire la casella di testo quando l'utente ci clicca sopra.
entry_field.bind("<FocusIn>", clear_entry)  # Evento di focus per ripulire la casella di input


entry_field.pack()
#creo il tasto invio e lo associo alla funzione send
send_button = tkt.Button(finestra, text="Invio", command=send)
#integro il tasto nel pacchetto
send_button.pack()


#----Connessione al Server----
#Da eseguire nella console dedicata
HOST = input('Inserire il Server host: ')
PORT = input('Inserire la porta del Server host: ')
if not PORT:
    PORT= 5000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
#avvia la Finestra Chat.
tkt.mainloop()
