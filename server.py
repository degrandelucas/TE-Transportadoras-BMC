# server.py
from flask import Flask, request, jsonify
from sheets_api import get_data_from_sheet

app = Flask(__name__)

@app.route('/consultar-transportadora', methods=['POST'])
def consultar_transportadora():
    cidade = request.json['cidade']
    try:
        dados = get_data_from_sheet(cidade)
        melhor_transportadora = encontrar_melhor_transportadora(dados)
        return jsonify({'transportadora': melhor_transportadora})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def encontrar_melhor_transportadora(dados):
    melhor_tempo = float('inf')
    melhor_transportadora = ''
    for row in dados:
        tempo = float(row[2])  # Ajuste o índice conforme a localização da coluna de tempo
        if tempo < melhor_tempo:
            melhor_tempo = tempo
            melhor_transportadora = row[1]  # Ajuste o índice conforme a localização da coluna de nome da transportadora
    return melhor_transportadora

if __name__ == '__main__':
    app.run(port=3000, debug=True)
