import requests
import random
from ascii_magic import AsciiArt
from PIL import Image
from io import BytesIO

# Sorteia ano e número da questão
ano = random.randint(2009, 2023)
numero = random.randint(1, 180)
url_api = f"https://api.enem.dev/v1/exams/{ano}/questions/{numero}"

try:
    response = requests.get(url_api)
    if response.status_code == 200:
        questoes = response.json()

        # Tenta pegar a imagem da questão sorteada
        if questoes.get("files"):
            img_url = questoes["files"][0] 
            img_res = requests.get(img_url)
            img = Image.open(BytesIO(img_res.content))
            img.show() 
            
            # OPÇÃO 2: Exibir no terminal (usando o ascii_magic que você importou)
            # art = AsciiArt.from_pillow(img)
            # art.to_terminal(columns=80)

        print("-" * 30)
        print(f"ENEM {ano} - Questão {numero}")
        print(f"Matéria: {questoes['discipline'].capitalize()}\n")
        print(f"{questoes['title']}\n")
        print(f"{questoes['context']}\n")

        for alt in questoes["alternatives"]:
            print(f"{alt['letter']}) {alt['text']}")
        
        print("-" * 30)
        resposta = input("Sua resposta: ").strip().lower()

        if resposta == questoes["correctAlternative"].lower():
            print("\n⭐ Mandou bem, nerd! Acertou.")
        else:
            print(f"\n❌ Errou! A correta era: {questoes['correctAlternative']}")
    else:
        print(f"Questão {numero} de {ano} não encontrada.")

except Exception as e:
    print(f"Erro inesperado: {e}")