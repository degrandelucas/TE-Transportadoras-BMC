# server.py
import os
import requests
from flask import Flask, request, jsonify
from sheets_api import get_data_from_sheet

app = Flask(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route('/consultar-transportadora', methods=['POST', 'OPTIONS'])
def consultar_transportadora():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        cidade = request.json.get('cidade')
        dados = get_data_from_sheet(cidade)
        prompt = criar_prompt_para_chatgpt(dados, cidade)
        transportadora = analisar_dados_com_chatgpt(prompt)
        if transportadora:
            return jsonify({'transportadora': transportadora})
        return jsonify({'error': 'Nenhuma transportadora encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def criar_prompt_para_chatgpt(dados, cidade):
    prompt = f"Analisar os seguintes dados de transportadoras para a cidade de {cidade} e determinar qual tem o menor tempo de entrega:\n"
    for linha in dados:
        prompt += f"Transportadora: {linha[1]}, Tempo de entrega: {linha[2]} dias.\n"
    prompt += "Qual é a melhor transportadora com base no menor tempo de entrega?"
    return prompt

def analisar_dados_com_chatgpt(prompt):
    headers = {'Authorization': f'Bearer {openai_api_key}'}
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json={'prompt': prompt, 'max_tokens': 150})
    response.raise_for_status()
    return response.json()['choices'][0]['text'].strip()

if __name__ == '__main__':
    app.run(port=3000, debug=True)
