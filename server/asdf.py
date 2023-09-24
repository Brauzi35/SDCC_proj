from flask import Flask, request, jsonify
from callLambda import *
from Prevision import *



app = Flask(__name__)



def prime_factors(n):
    factors = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

#sto aggiungendo questa funzione
@app.route('/esegui-funzione', methods=['POST'])
def esegui_funzione():
    print("funzione in esecuzione")
    try:
        # Ricevi i dati dalla richiesta HTTP come JSON
        data = request.get_json()

        # Estrai la stringa di input dalla richiesta
        input_string = data['input']

        # Merge con aws
        prediction = predict(int(input_string))
        if prediction > 1.0:
            risultato = 'lambda'
            return jsonify({'risultato': risultato})
        else:
            # Esegui la tua funzione
            risultato = prime_factors(int(input_string))

            # Restituisci il risultato come JSON
            return jsonify({'risultato': risultato})

    except Exception as e:
        return jsonify({'errore': str(e)})





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

