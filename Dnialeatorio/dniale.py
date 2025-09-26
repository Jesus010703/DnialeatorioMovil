from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)

URL = "https://api.consultasperu.com/api/v1/query"
TOKEN = "f7ba1cc80c40836961badf19660831ffc3489d200e89a56674b54d135a7c86ab"

def calcular_digito_luhn(numero):
    suma = 0
    invertir = True
    for digito in reversed(numero):
        d = int(digito)
        if invertir:
            d *= 2
            if d > 9:
                d -= 9
        suma += d
        invertir = not invertir
    return str((10 - (suma % 10)) % 10)

def generar_dni_con_luhn_inicio_valido():
    primer_digito = random.choice(['1', '4', '7'])
    otros_digitos = ''.join(str(random.randint(0, 9)) for _ in range(6))
    base_dni = primer_digito + otros_digitos
    digito_luhn = calcular_digito_luhn(base_dni)
    return base_dni + digito_luhn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultar', methods=['POST'])
def consultar():
    dni = request.json.get("dni")
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": TOKEN,
        "type_document": "dni",
        "document_number": dni
    }
    response = requests.post(URL, headers=headers, json=payload)
    return jsonify(response.json())

if __name__ == "__main__":

    app.run(debug=True)


