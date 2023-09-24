import tkinter as tk
from tkinter import scrolledtext

import requests

#from client import *
from PIL import Image, ImageTk
from discovery import *

import configparser

# Crea un oggetto ConfigParser e leggi il file di configurazione
config = configparser.ConfigParser()
config.read('config.ini')

ip = ""
port = ""
df = read_csv_from_s3(bucket_name, csv_key)
if df is not None and not df.empty:

    index_min_connections = df['connections'].idxmin()
    # Estrai indirizzo IP e porta del server con meno connessioni attive
    ip = df.loc[index_min_connections, 'ip']
    port = df.loc[index_min_connections, 'port']

    df.loc[index_min_connections, 'connections'] += 1

    # Sovrascrivi il CSV su S3 con il DataFrame aggiornato
    updated_csv = df.to_csv(index=False)
    s3.put_object(Bucket=bucket_name, Key=csv_key, Body=updated_csv)

    print(f'Primo indirizzo IP: {ip}')
    print(f'Prima porta: {port}')
else:
    print('Il DataFrame è vuoto o non è stato possibile leggerlo dal CSV.')

# Accedi alle configurazioni
numero_primi_url = "http://"+ str(ip) + ":" + str(port) + config['Server']['numero_primi_url']
factorial_url = "http://"+ str(ip) + ":" + str(port) + config['Server']['factorial_url']
pi_url = "http://"+ str(ip) + ":" + str(port) + config['Server']['pi_url']


var = 0


def on_closing():
    df.loc[index_min_connections, 'connections'] -= 1

    # Sovrascrivi il CSV su S3 con il DataFrame aggiornato
    updated_csv = df.to_csv(index=False)
    s3.put_object(Bucket=bucket_name, Key=csv_key, Body=updated_csv)
    root.destroy()


def cambia_testo(nuovo_testo):
    labelRes.delete("1.0", "end")  # Cancella il contenuto attuale del widget Text
    labelRes.insert("1.0", nuovo_testo)  # Inserisci il nuovo testo
# Funzione da eseguire quando il pulsante interno viene premuto
def stampa_testo():
    testo = entry.get()
    print("Testo inserito: " + testo)
def hide_init():
    label_iniziale.pack_forget()
    button1.pack_forget()
    button2.pack_forget()
    button3.pack_forget()
# Funzione per passare dalla schermata iniziale alla schermata con la casella di testo
def mostra_casella_di_testo(): #prime_factors

    hide_init()
    #show
    label_testo.pack()
    entry.pack()
    button_container.pack()
    button_back.pack()
    global var
    var = 1

def mostra_isprime(): #isprime
    hide_init()
    label_testo_isprime.pack()
    entry_isprime.pack()
    button_container_isprime.pack()
    button_back_isprime.pack()
    global var
    var = 2

def mostra_fact(): #factorial
    hide_init()
    label_testo_fact.pack()
    entry_fact.pack()
    button_container_fact.pack()
    button_back_fact.pack()
    global var
    var = 3

def finestra_iniziale():
    label_testo.pack_forget()
    entry.pack_forget()
    button_stampa.pack_forget()
    button_container.pack_forget()
    button_back.pack_forget()
    label_testo_isprime.pack_forget()
    entry_isprime.pack_forget()
    button_container_isprime.pack_forget()
    button_back_isprime.pack_forget()
    label_testo_fact.pack_forget()
    entry_fact.pack_forget()
    button_container_fact.pack_forget()
    button_back_fact.pack_forget()
    button1.pack(pady = 10)
    button2.pack(pady = 10)
    button3.pack(pady = 10)
    labelRes.pack_forget()
    global var
    var = 0

def crea_container():
    global var
    if var == 1: #primefactors
        txt = entry.get()
        if txt.isdigit() and int(txt) >= 0:
            response = requests.post(numero_primi_url, json={'input': txt})
            risultato = response.json().get('risultato', 'Errore')
            print(risultato)
            cambia_testo(str(risultato))
            labelRes.pack()
        else:
            cambia_testo("sono ammessi solo numeri interi")
            labelRes.pack()
    elif var == 2: #pi
        txt = entry_isprime.get()
        if txt.isdigit() and int(txt) >= 0:
            response = requests.post(pi_url, json={'input': txt})
            risultato = response.json().get('risultato', 'Errore')
            print(risultato)
            cambia_testo(str(risultato))
            labelRes.pack()
        else:
            cambia_testo("sono ammessi solo numeri interi")
            labelRes.pack()
    elif var == 3: #fact
        txt = entry_fact.get()
        if txt.isdigit() and int(txt) >= 0:
            response = requests.post(factorial_url, json={'input': txt})
            risultato = response.json().get('risultato', 'Errore')
            print(risultato)
            cambia_testo(str(risultato))
            labelRes.pack()
        else:
            print('devi inserire solo numeri sveglione')
            cambia_testo("sono ammessi solo numeri interi")
            labelRes.pack()





# Crea la finestra principale
root = tk.Tk()
root.title("Big problems, light solutions")
root.geometry("500x190") #deco
root.resizable(width=False, height=False)

# Registra la funzione on_closing come gestore dell'evento di chiusura
root.protocol("WM_DELETE_WINDOW", on_closing)

# Carica una sequenza di immagini GIF come sfondo animato
sfondo_gif = []
for i in range(0, 71):  # Sostituisci con il numero di frame della tua GIF
    frame = Image.open(f"wallpaper/frame_{i}_delay-0.03s.gif")  # Sostituisci con il percorso dei tuoi frame GIF
    sfondo_gif.append(ImageTk.PhotoImage(frame))

# Crea una label per visualizzare le immagini GIF

sfondo_label = tk.Label(root)
sfondo_label.place(relwidth=1, relheight= 1)

labelRes = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=30, height=10)
labelRes.config(background='purple', foreground='white')



# Funzione per aggiornare il frame GIF
def update_gif(frame_idx=0):
    sfondo_label.config(image=sfondo_gif[frame_idx])
    root.after(100, update_gif, (frame_idx + 1) % len(sfondo_gif))

# Avvia l'aggiornamento del frame GIF
update_gif()

# Stile dei pulsanti
pulsante_stile = {

    "font": ("Helvetica", 12),
    "padx": 10,
    "pady": 5,
    "bg": "purple",  # Colore di sfondo
    "fg": "white",   # Colore del testo
    "borderwidth": 2,
    "relief": "raised"  # Effetto rialzato
}


# Crea due frame, uno per la schermata iniziale e uno per la schermata con la casella di testo



# Schermata iniziale con 4 pulsanti
label_iniziale = tk.Label(root, text="Schermata Iniziale")
button1 = tk.Button(root, text="Mostra Fattorizzazione", command=mostra_casella_di_testo, **pulsante_stile)
button2 = tk.Button(root, text="Mostra Cifre PiGreco", command= mostra_isprime, **pulsante_stile)
button3 = tk.Button(root, text="Mostra Calcola Fattoriale", command= mostra_fact, **pulsante_stile)


# Posiziona gli elementi sulla schermata iniziale
button1.pack(pady = 10)
button2.pack(pady = 10)
button3.pack(pady = 10)

# Schermata con la casella di testo - numeri primi
label_testo = tk.Label(root, text="Trova i fattori primi di un numero")
entry = tk.Entry(root)  # Casella di testo
button_stampa = tk.Button(root, text="Stampa Testo", command=stampa_testo, **pulsante_stile)
button_container = tk.Button(root, text="Compute", command=crea_container, **pulsante_stile)
button_back = tk.Button(root, text="Back", command=finestra_iniziale, **pulsante_stile)


# Schermata con la casella di testo - isprime
label_testo_isprime = tk.Label(root, text="Trova l'ennesima cifra del pigreco")
entry_isprime = tk.Entry(root)  # Casella di testo
button_container_isprime = tk.Button(root, text="Compute", command=crea_container, **pulsante_stile)
button_back_isprime = tk.Button(root, text="Back", command=finestra_iniziale, **pulsante_stile)



# Schermata con la casella di testo - isprime
label_testo_fact = tk.Label(root, text="Trova il fattoriale del numero inserito")
entry_fact = tk.Entry(root)  # Casella di testo
button_container_fact = tk.Button(root, text="Compute", command=crea_container, **pulsante_stile)
button_back_fact = tk.Button(root, text="Back", command=finestra_iniziale, **pulsante_stile)


# Avvia l'applicazione
root.mainloop()
