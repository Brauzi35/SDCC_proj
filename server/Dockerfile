# Usa l'immagine di Python
FROM python:3.9

# Copia il codice Python nel container
COPY asdf.py /app/asdf.py
COPY callLambda.py /app/callLambda.py
COPY Prevision.py /app/Prevision.py
COPY fattori_primi2.csv /app/fattori_primi2.csv

# Imposta la directory di lavoro
WORKDIR /app

# Installa le dipendenze se ne hai bisogno (in questo caso, Flask)
RUN pip install flask
RUN pip install boto3
RUN pip install scikit-learn
RUN pip install pandas
RUN pip install numpy

# Esponi la porta 5000 per le richieste HTTP
#EXPOSE 5000
#EXPOSE 512

# Esegui il codice Python quando il container viene avviato
CMD ["python", "asdf.py"]

