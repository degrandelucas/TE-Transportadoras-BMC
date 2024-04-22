# server.py
import os
import requests
from flask import Flask, request, jsonify
from sheets_api import get_data_from_sheet

app = Flask(__name__)

# Substitua 'your_api_key_here' pela sua chave de API real da OpenAI.
# openai_api_key = os.getenv("OPENAI_API_KEY", "sk-proj-QcKDZF9MdpycqMHgLKCTT3BlbkFJLbOTG2B51HgrEq8jFi1D")

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
        prompt = criar_prompt_para_chatgpt(dados, cidade)
        melhor_transportadora, detalhes = analisar_dados_com_chatgpt(prompt)

        # Verifica se uma transportadora foi encontrada
        if melhor_transportadora:
            return jsonify({'transportadora': melhor_transportadora, 'detalhes': detalhes})
        else:
            return jsonify({'error': 'Nenhuma transportadora encontrada para a cidade especificada'}), 404
    except Exception as e:
        print("Erro durante a consulta:", e)  # Logs detalhados para diagnóstico
        return jsonify({'error': str(e)}), 500

def criar_prompt_para_chatgpt(dados, cidade):
    # Transforma os dados da planilha em uma prompt legível pelo GPT-3
    prompt = f"Dada a seguinte lista de transportadoras e seus tempos de entrega para a cidade {cidade}:\n"
    for linha in dados:
        transportadora, tempo = linha[1], linha[2]
        prompt += f"Transportadora {transportadora}, Tempo de entrega: {tempo} dias.\n"
    prompt += "Qual é a melhor transportadora com base no menor tempo de entrega?"
    return prompt

def analisar_dados_com_chatgpt(prompt):
    response = requests.post(
        "https://api.openai.com/v1/engines/davinci-codex/completions",
        headers={
            "Authorization": f"Bearer {openai_api_key}"
        },
        json={
            "prompt": prompt,
            "max_tokens": 150
        }
    )
    response.raise_for_status()
    content = response.json()
    resposta_chatgpt = content['choices'][0]['text'].strip()

    # Aqui você precisará adaptar o código para extrair a informação relevante da resposta do ChatGPT
    # Exemplo: Supondo que a resposta seja uma string contendo o nome da melhor transportadora
    # melhor_transportadora = resposta_chatgpt.split(':')[1].strip()
    # detalhes = "Detalhes adicionais que você possa querer incluir"

    return resposta_chatgpt, "Detalhes adicionais sobre a decisão."

if __name__ == '__main__':
    app.run(port=3000, debug=True)
