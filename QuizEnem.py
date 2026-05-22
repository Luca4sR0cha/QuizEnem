import requests
import random
import time
from PIL import Image
from io import BytesIO
from pytimedinput import timedInput

# IA


# API ENEM
URL_BASE = "https://api.enem.dev/v1/exams"

# --- SELEÇÃO DE DIFICULDADE ---
print("Selecione a dificuldade:")
print("1 - Fácil (3 alternativas)")
print("2 - Média (4 alternativas)")
print("3 - Difícil (5 alternativas)")

while True:
    opcao = input("Opção: ").strip()
    if opcao in ["1", "2", "3"]:
        # Define quantas alternativas devem aparecer
        num_alternativas = { "1": 3, "2": 4, "3": 5 }[opcao]
        break
    print("Opção inválida! Escolha 1, 2 ou 3.")
# ------------------------------

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

        # Tenta pegar a imagem da questão sorteada
        if questao.get("files"):
            img_url = questao["files"][0] 
            img_res = requests.get(img_url)
            img = Image.open(BytesIO(img_res.content))
            img.show() 
            # OPÇÃO 2: Exibir no terminal (usando o ascii_magic)
            # art = AsciiArt.from_pillow(img)
            # art.to_terminal(columns=80)

        print("\n" + "-" * 50)
        print(f"ENEM {ano} - Questão {numero}")
        print(f"Matéria: {questao['discipline'].capitalize()}")
        print("-" * 50)

        # pergunta
        print(f"\n{questao['title']}\n")
        print(f"{questao['context']}\n")

        # --- FILTRAGEM DAS ALTERNATIVAS POR DIFICULDADE ---
        correta_letra = questao["correctAlternative"].lower()
        alternativas_originais = questao["alternatives"]
        
        # Separa a correta das incorretas
        alt_correta = [a for a in alternativas_originais if a['letter'].lower() == correta_letra]
        alt_incorretas = [a for a in alternativas_originais if a['letter'].lower() != correta_letra]
        
        # Define quantas incorretas precisamos manter (Ex: se quer 3 no total, mantém 2 incorretas)
        qtd_incorretas_manter = num_alternativas - 1
        
        # Sorteia as incorretas que vão ficar e junta com a correta
        alt_filtradas = alt_correta + random.sample(alt_incorretas, qtd_incorretas_manter)
        
        # Reordena de A a E para não entregar a resposta pela posição
        alt_filtradas.sort(key=lambda x: x['letter'])
        # --------------------------------------------------

        # alternativas (agora usando a lista filtrada)
        for alt in alt_filtradas:
            print(f"{alt['letter']}) {alt['text']}")

        # resposta do usuário
        print(f"\nSua resposta (você tem 60s):")
        # timeout=60 define o tempo, e o input é lido em 'resposta'
        resposta_bruta, timedOut = timedInput("> ", timeout=180)

        resposta = resposta_bruta.strip().lower()

        # Valida se o usuário escolheu uma alternativa que está visível
        letras_visiveis = [a['letter'].lower() for a in alt_filtradas]
        if resposta not in letras_visiveis:
            print("\n⚠️ Essa alternativa não estava entre as opções válidas!")
            continue

        correta = questao["correctAlternative"].lower()

        # Pequena pausa para suspense
        import time
        time.sleep(1) 

        # verifica
        if resposta == correta:
            print("\n⭐ Acertou!")
        
        elif timedOut:
            print("\n\n⏰ TEMPO ESGOTADO! Você demorou para responder.")
            
        else:
            print(f"\n❌ Errou! Estuda mais que o ENEM tá chegando!")
            print(f"Resposta correta: {correta.upper()}")

        continuar = input("\nContinuar? (s/n): ").lower()
        if continuar == "n":
            break

    except Exception as e:
        print(f"\nErro: {e}")