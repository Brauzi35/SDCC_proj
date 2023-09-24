import csv

import boto3
import pandas as pd
from io import StringIO, BytesIO

# Configura il client S3
s3 = boto3.client('s3')

# Nome del tuo bucket S3 e percorso del CSV all'interno del bucket
bucket_name = 'discoveryservice1'
csv_key = 'disc.csv'  # Assicurati di specificare il nome corretto del tuo file CSV

# Leggi il file CSV da S3
def read_csv_from_s3(bucket_name, csv_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=csv_key)
        csv_content = response['Body'].read().decode('utf-8')
        # Utilizza pandas per analizzare il CSV
        df = pd.read_csv(StringIO(csv_content))
        return df
    except Exception as e:
        print(f'Errore nel recupero del CSV da S3: {e}')
        return None



def write_csv(ip, port):

    connections = 0

    # Inizializza il client S3
    s3 = boto3.client('s3')

    # Scarica il file CSV dal bucket
    response = s3.get_object(Bucket=bucket_name, Key=csv_key)

    # Leggi il contenuto del file CSV
    csv_data = response['Body'].read().decode('utf-8')

    # Usa StringIO per lavorare con i dati CSV come se fosse un file
    csv_buffer = StringIO(csv_data)
    csv_reader = csv.reader(csv_buffer)

    # Converti il CSV in una lista di righe
    csv_rows = list(csv_reader)

    # Aggiungi una nuova riga con i dati
    new_row = [ip, str(port), str(connections)]
    csv_rows.append(new_row)

    # Scrivi il nuovo CSV in una stringa
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(csv_rows)

    # Carica il nuovo CSV nell'bucket S3 sovrascrivendo il file esistente
    s3.put_object(Bucket=bucket_name, Key=csv_key, Body=csv_buffer.getvalue(), ContentType='text/csv')

def shutdown(ip_to_remove):
    # Inizializza il client S3
    s3 = boto3.client('s3')

    # Scarica il file CSV dal bucket
    response = s3.get_object(Bucket=bucket_name, Key=csv_key)

    # Leggi il contenuto del file CSV
    csv_data = response['Body'].read().decode('utf-8')

    csv_reader = csv.DictReader(csv_data.splitlines())
    fieldnames = csv_reader.fieldnames
    rows = [row for row in csv_reader if row['ip'] != ip_to_remove]

    # Sovrascrivi il file CSV su S3 con le righe rimanenti
    csv_buffer = BytesIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(rows)

    # Carica il nuovo file CSV su S3
    s3.put_object(Bucket=bucket_name, Key=csv_key, Body=csv_buffer.getvalue())

df = read_csv_from_s3(bucket_name, csv_key)
if df is not None and not df.empty:
    # Estrai il primo indirizzo IP e la prima porta
    primo_indirizzo_ip = df.loc[0, 'ip']
    prima_porta = df.loc[0, 'port']

    print(f'Primo indirizzo IP: {primo_indirizzo_ip}')
    print(f'Prima porta: {prima_porta}')
else:
    print('Il DataFrame è vuoto o non è stato possibile leggerlo dal CSV.')