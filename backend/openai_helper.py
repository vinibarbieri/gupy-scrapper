import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def gerar_resposta_openai(pergunta):
    try:
        system_prompt = (
            "Você é um assistente que responde formulários de candidatura de emprego. "
            "Responda de forma profissional e objetiva, de acordo com a pergunta. "
            "Se for pergunta de múltipla escolha, responda apenas com a melhor opção."
        )

        resposta = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pergunta},
            ],
            temperature=0.2,
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Erro na OpenAI: {e}")
        return "Não informado"
