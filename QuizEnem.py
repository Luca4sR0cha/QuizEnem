import requests
import random
from openai import OpenAI

# IA
client_openAI = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

# API ENEM
URL_BASE = "https://api.enem.dev/v1/exams"

while True:

    # sorteia questão
    ano = random.randint(2009, 2023)
    numero = random.randint(1, 180)

    url_api = f"{URL_BASE}/{ano}/questions/{numero}"

    try:

        response = requests.get(url_api)

        if response.status_code != 200:
            print("Erro ao pegar questão.\n")
            continue

        questao = response.json()

        print("\n" + "-" * 50)
        print(f"ENEM {ano} - Questão {numero}")
        print(f"Matéria: {questao['discipline'].capitalize()}")
        print("-" * 50)

        # pergunta
        print(f"\n{questao['title']}\n")
        print(f"{questao['context']}\n")

        # alternativas
        for alt in questao["alternatives"]:

            print(f"{alt['letter']}) {alt['text']}")

        # resposta do usuário
        resposta = input("\nSua resposta: ").strip().lower()

        correta = questao["correctAlternative"].lower()

        # verifica
        if resposta == correta:

            print("\n⭐ Acertou!")

        else:

            print(f"\n❌ Errou faz enem!")
            print(f"Resposta correta: {correta.upper()}")

            usar_ia = input(
                "\nQuer explicação da IA? (s/n): "
            ).lower()

            # IA explica
            if usar_ia == "s":

                print("\nIA pensando...\n")

                resposta_ia = client_openAI.chat.completions.create(
                    model="google/gemma-3-1b",
                    messages=[
                        {
                            "role": "system",
                            "content": "Você é um professor didático"
                        },
                        {
                            "role": "user",
                            "content": f"""
                            Explique essa questão:

                            Matéria:
                            {questao['discipline']}

                            Questão:
                            {questao['title']}

                            Texto:
                            {questao['context']}

                            Alternativas:
                            {questao['alternatives']}

                            Correta:
                            {questao['correctAlternative']}

                            Minha resposta:
                            {resposta}

                            Explique de forma simples.
                            """
                        }
                    ],
                    temperature=0.7
                )

                print(resposta_ia.choices[0].message.content)

        continuar = input("\nContinuar? (s/n): ").lower()

        if continuar != "s":
            break

    except Exception as e:

        print(f"\nErro: {e}")