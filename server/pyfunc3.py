from flask import Flask, request, jsonify


app = Flask(__name__)


def factorial(n):
    if n < 0:
        return "Il fattoriale è definito solo per numeri non negativi."
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

@app.route('/esegui-funzione3', methods=['POST'])
def esegui_funzione():
    print("funzione in esecuzione")
    try:
        # Ricevi i dati dalla richiesta HTTP come JSON
        data = request.get_json()

        # Estrai la stringa di input dalla richiesta
        input_string = data['input']

        # Esegui la tua funzione
        risultato = factorial(int(input_string))

        # Restituisci il risultato come JSON
        return jsonify({'risultato': risultato})

    except Exception as e:
        return jsonify({'errore': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)