# server.py
from flask import Flask, request, jsonify
from sheets_api import get_data_from_sheet

app = Flask(__name__)

@app.route('/consultar-transportadora', methods=['POST', 'OPTIONS'])
def consultar_transportadora():
    if request.method == 'OPTIONS':
        return '', 200  # A resposta para OPTIONS deve ser 200 OK.
    
    try:
        # Verifica se o corpo da requisição contém 'cidade'
        if not request.json or 'cidade' not in request.json:
            return jsonify({'error': 'Cidade não fornecida'}), 400

        cidade = request.json['cidade']
        dados = get_data_from_sheet(cidade)
        melhor_transportadora = encontrar_melhor_transportadora(dados)

        # Verifica se uma transportadora foi encontrada
        if melhor_transportadora:
            return jsonify({'transportadora': melhor_transportadora})
        else:
            return jsonify({'error': 'Nenhuma transportadora encontrada para a cidade especificada'}), 404
    except Exception as e:
        print("Erro durante a consulta:", e)  # Logs detalhados para diagnóstico
        return jsonify({'error': str(e)}), 500

def encontrar_melhor_transportadora(dados):
    melhor_tempo = float('inf')
    melhor_transportadora = ''
    for row in dados:
        try:
            tempo = float(row[2])  # Ajuste o índice conforme a localização da coluna de tempo
            if tempo < melhor_tempo:
                melhor_tempo = tempo
                melhor_transportadora = row[1]  # Ajuste o índice conforme a localização da coluna de nome da transportadora
        except (IndexError, ValueError) as e:
            print(f"Erro ao processar dados: {e}")
            continue  # Ignora linhas com dados incompletos ou mal formatados
    return melhor_transportadora

if __name__ == '__main__':
    app.run(port=3000, debug=True)