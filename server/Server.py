import threading
import requests
import docker
from flask import Flask, request, jsonify
import configparser
import datetime
import time
from discovery import *

from server.callLambda import *

string = None

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('server_config.ini')

datePN = None
datePi = None
dateF = None

def gb_thread():
    client = docker.from_env()
    while True:
        print(datePi)
        containerPi = client.containers.get("pi")
        containerPN = client.containers.get("prime_numbers")
        containerF = client.containers.get("factorial")
        if datePi is not None:
            curr = datetime.datetime.now()
            dif = curr - datePi
            if dif.total_seconds() > 200:
                containerPi.remove()
            elif dif.total_seconds() > 60:
                containerPi.stop()
        if datePN is not None:
            curr = datetime.datetime.now()
            dif = curr - datePN
            if dif.total_seconds() > 200:
                containerPN.remove()
            elif dif.total_seconds() > 60:
                containerPN.stop()
        if dateF is not None:
            curr = datetime.datetime.now()
            dif = curr - dateF
            if dif.total_seconds() > 200:
                containerF.remove()
            elif dif.total_seconds() > 60:
                containerF.stop()
        time.sleep(10)



def build_and_run_container(image_name, dockerfile_path, docker_absolute,container_name ,ports_mapping=None):
    client = docker.from_env()

    try:
        #Build the Docker image from the Dockerfile
        image, build_logs = client.images.build(path=dockerfile_path, dockerfile=docker_absolute, tag=image_name)

        container = client.containers.run(
            image=image_name,
            ports=ports_mapping,
            detach=True,
            name=container_name
        )
        result = container.logs().decode("utf-8")  # Otteniamo i log del container

        global string




        container.title()

        string = container.attrs['NetworkSettings']['IPAddress']
        print("stringa è " + string)
        container.wait()
        container.remove()

        return result

    except docker.errors.BuildError as e:
        print("Build failed:", e.build_log)
        print(build_logs)
    except docker.errors.ContainerError as e:
        print("Container failed:", e.stderr)
    except Exception as e:
        print("An error occurred:", e)

    return None

def call_go_function_1(image_name, port):



    docker_absolute = ""

    dockerfile_path = config['Server']['df_path']

    container_name = "error"

    if port == config['Server']['port_pn']:
        docker_absolute = config['Server']['pn_abs']
        container_name = 'prime_numbers'
    elif port == config['Server']['port_f']:
        docker_absolute = config['Server']['f_abs']
        container_name = 'factorial'
    elif port == config['Server']['port_pi']:
        docker_absolute = config['Server']['pi_abs']
        container_name = 'pi'
    ports_mapping = {
        int(port) : int(port)
    }
    print(docker_absolute)

    container = build_and_run_container(image_name, dockerfile_path, docker_absolute, container_name,ports_mapping)

    if container:
        print("Container creato e in esecuzione:", container)
    else:
        print("Creazione del container fallita.")


def avvio_numeri_primi(input_string):
    global datePN
    datePN = datetime.datetime.now()
    # Inizializza il client Docker
    client = docker.from_env()

    # Cerca il container desiderato tra quelli attivi o in stato "exited"
    container = None
    for c in client.containers.list(all=True, filters={"name": "prime_numbers"}):
        if c.status in ("running", "restarting", "exited"):
            container = c
            break

    if container:
        # Se il container è attivo o in stato "exited", riavvialo
        if container.status == "exited":
            container.restart()
    else:
        # Se il container non esiste, crea un nuovo container e avvialo
        print("entrato nell'else")
        call_go_function_1("pyfunc.py", config['Server']['port_pn'])

    # URL del server nel container
    server_url = 'http://' + str(config['Server']['ip2']) + ':' + str(config['Server']['port_pn']) + '/esegui-funzione'
    print(server_url)


    # Esegui una richiesta HTTP POST al server
    response = requests.post(server_url, json={'input': input_string})

    # Verifica la risposta
    if response.status_code == 200:
        risultato = response.json().get('risultato', 'Errore')
        if risultato == 'lambda':
            res = startLambda(int(input_string), 'FactorizeLambda')
            # Decodifica il testo JSON
            json_data = json.loads(res.decode('utf-8'))

            # Estrae la lista di fattori
            factors = json.loads(json_data['body'])['factors']
            print("Risultato lambda:", factors)
            return factors
        else:
            print("Risultato:", risultato)
            return risultato
    else:
        print("Errore nella richiesta HTTP:", response.status_code)


def avvio_factorial(input_string):
    global dateF
    dateF = datetime.datetime.now()

    # Inizializza il client Docker
    client = docker.from_env()

    # Cerca il container desiderato tra quelli attivi o in stato "exited"
    container = None
    for c in client.containers.list(all=True, filters={"name": "factorial"}):
        if c.status in ("running", "restarting", "exited"):
            container = c
            break

    if container:
        # Se il container è attivo o in stato "exited", riavvialo
        if container.status == "exited":
            container.restart()
    else:
        # Se il container non esiste, crea un nuovo container e avvialo
        print("entrato nell'else")
        call_go_function_1("factorial", config['Server']['port_f'])

    #call_go_function_1()

    # URL del server nel container
    #server_url = 'http://localhost:8000/esegui-funzione3' #con 5000 mi chiama l'altro container
    server_url = 'http://' + str(config['Server']['ip2']) + ':' + str(config['Server']['port_f']) + '/esegui-funzione3'

    print(server_url)

    # Stringa da inviare alla funzione nel container
    #input_string = '1235643564453'

    # Esegui una richiesta HTTP POST al server
    response = requests.post(server_url, json={'input': input_string})

    # Verifica la risposta
    if response.status_code == 200:
        if int(input_string) > 1000:
            res = startLambda(int(input_string), 'FactorialLambda')
            json_data = json.loads(res.decode('utf-8'))

            # Estrae la lista di fattori
            fact = json_data['body']['Fattoriale (Approssimato)']
            print("Risultato lambda:", fact)
            return fact
        else:
            risultato = response.json().get('risultato', 'Errore')
            print("Risultato:", risultato)
            return risultato
    else:
        print("Errore nella richiesta HTTP:", response.status_code)


def avvio_pi(input_string):
    # Inizializza il client Docker
    global datePi
    datePi = datetime.datetime.now()

    client = docker.from_env()


    # Cerca il container desiderato tra quelli attivi o in stato "exited"
    container = None
    for c in client.containers.list(all=True, filters={"name": "pi"}):
        if c.status in ("running", "restarting", "exited"):
            container = c
            break

    if container:
        # Se il container è attivo o in stato "exited", riavvialo
        if container.status == "exited":
            container.restart()
    else:
        # Se il container non esiste, crea un nuovo container e avvialo
        print("entrato nell'else")
        call_go_function_1("pi", config['Server']['port_pi'])

    #call_go_function_1()

    # URL del server nel container
    server_url = 'http://' + str(config['Server']['ip2']) + ':' + str(config['Server']['port_pi']) + '/esegui-funzione4'

    print(server_url)


    # Esegui una richiesta HTTP POST al server
    response = requests.post(server_url, json={'input': input_string})

    # Verifica la risposta
    if response.status_code == 200:
        if int(input_string) > 100:
            res = startLambda(int(input_string), 'PiLambda')
            json_data = json.loads(res.decode('utf-8'))

            # Estrae la lista di fattori
            pi = json.loads(json_data['body'])['pi']
            print("Risultato lambda:", pi)
            return pi
        else:
            risultato = response.json().get('risultato', 'Errore')
            print("Risultato:", risultato)
            return risultato
    else:
        print("Errore nella richiesta HTTP:", response.status_code)

@app.route('/avvio_numeri_primi', methods=['POST'])
def serverFactorize():
    try:
        # Ricevi i dati dalla richiesta HTTP come JSON
        data = request.get_json()

        # Estrai la stringa di input dalla richiesta
        input_string = data['input']

        # Esegui la tua funzione
        risultato = avvio_numeri_primi(input_string)
        print("dal server leggiamo",risultato)
        # Restituisci il risultato come JSON
        return jsonify({'risultato': risultato})

    except Exception as e:
        return jsonify({'errore': str(e)})


@app.route('/avvio_pi', methods=['POST'])
def serverPi():
    try:
        # Ricevi i dati dalla richiesta HTTP come JSON
        data = request.get_json()

        # Estrai la stringa di input dalla richiesta
        input_string = data['input']

        # Esegui la tua funzione
        risultato = avvio_pi(input_string)
        print("dal server leggiamo",risultato)
        # Restituisci il risultato come JSON
        return jsonify({'risultato': risultato})

    except Exception as e:
        return jsonify({'errore': str(e)})


@app.route('/avvio_factorial', methods=['POST'])
def serverFactorial():
    try:
        # Ricevi i dati dalla richiesta HTTP come JSON
        data = request.get_json()

        # Estrai la stringa di input dalla richiesta
        input_string = data['input']

        # Esegui la tua funzione
        risultato = avvio_factorial(input_string)
        print("dal server leggiamo",risultato)
        # Restituisci il risultato come JSON
        return jsonify({'risultato': risultato})

    except Exception as e:
        return jsonify({'errore': str(e)})



if __name__ == '__main__':
    port = config['Server']['port']
    ip = config['Server']['ip']

    #setup back-end discovery
    #write_csv(ip, port)

    # Avvia il server Flask su un thread separato
    server_thread = threading.Thread(target=lambda: app.run(host=ip, port=port))
    server_thread.start()

    # Avvia il garbage collector thread
    garbage_collector_thread = threading.Thread(target=gb_thread)
    garbage_collector_thread.start()
