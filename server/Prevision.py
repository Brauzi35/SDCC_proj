import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression



def predict(valore_da_predire):
    # Carica il CSV in un DataFrame
    df = pd.read_csv('fattori_primi2.csv')

    # Estrai le colonne "Input" e "Time"
    input_values = df['Input'].values
    time_values = df['Time'].values

    # Reshape in un array 2D con una singola colonna (necessario per sklearn)
    input_values_2d = input_values.reshape(-1, 1)

    # Crea un modello di regressione lineare
    model = LinearRegression()

    # Addestra il modello sui dati di addestramento
    model.fit(input_values_2d, time_values)
    #valore_da_predire=2345678234433
    # Fai previsioni per un dato input
    input_to_predict = np.array([[valore_da_predire]])  # Sostituisci con il valore da predire
    predicted_time = model.predict(input_to_predict)

    # Stampa la previsione
    print(f'Tempo di Esecuzione stimato per l\'input {valore_da_predire}: {predicted_time[0]}')
    return predicted_time



