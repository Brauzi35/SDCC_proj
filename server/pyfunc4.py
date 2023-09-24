import decimal
import math
from flask import Flask, request, jsonify


app = Flask(__name__)

def calculate_pi(digits):
    decimal.getcontext().prec = digits + 2  # Imposta la precisione dei calcoli decimali

    a = decimal.Decimal(1)
    b = decimal.Decimal(1) / decimal.Decimal(2).sqrt()
    t = decimal.Decimal(0.25)
    p = decimal.Decimal(1)

    for _ in range(digits):
        a_next = (a + b) / 2
        b = (a * b).sqrt()
        t -= p * (a - a_next) * (a - a_next)
        a = a_next
        p *= 2

    pi = (a + b) * (a + b) / (4 * t)

    return str(pi)[:-1]  # Restituisci π senza l'ultimo cifra 3, che è fissa


@app.route('/esegui-funzione4', methods=['POST'])
def esegui_funzione():
    print("funzione in esecuzione")
    try:
        # Ricevi i dati dalla richiesta HTTP come JSON
        data = request.get_json()

        # Estrai la stringa di input dalla richiesta
        input_string = data['input']

        # Esegui la tua funzione
        risultato = calculate_pi(int(input_string))

        # Restituisci il risultato come JSON
        return jsonify({'risultato': risultato})

    except Exception as e:
        return jsonify({'errore': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
#print(f"π con {num_cifre} cifre decimali:\n{pi_calcolato}")
