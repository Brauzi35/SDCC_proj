import math
from flask import Flask, request, jsonify


app = Flask(__name__)


def is_prime(number):
    if number <= 1:
        return False
    elif number <= 3:
        return True
    elif number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True


@app.route('/esegui-funzione2', methods=['POST'])
def esegui_funzione2():
    print("funzione in esecuzione")
    try:
        # Ricevi i dati dalla richiesta HTTP come JSON
        data = request.get_json()

        # Estrai la stringa di input dalla richiesta
        input_string = data['input']

        # Esegui la tua funzione
        risultato = is_prime(int(input_string))

        # Restituisci il risultato come JSON
        return jsonify({'risultato': risultato})

    except Exception as e:
        return jsonify({'errore': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)