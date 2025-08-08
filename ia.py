# ia.py
import requests

API_KEY = "SUA CHAVE DE API I.A AQUI"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def responder_pergunta(pergunta):
    system_message = "Você é uma assistente que responde todas as perguntas somente em português do Brasil, de forma clara e objetiva."

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": pergunta}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)

        if response.status_code == 200:
            resposta = response.json()['choices'][0]['message']['content'].strip()
            return resposta
        else:
            print("Erro na API:", response.status_code, response.text)
            return "Desculpe, não consegui responder agora."
    except Exception as e:
        print("Erro de requisição:", e)
        return "Ocorreu um erro ao acessar a inteligência artificial."
