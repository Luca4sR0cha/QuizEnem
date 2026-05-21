import tkinter as tk
from tkinter import messagebox
import requests
import random
import threading

from PIL import Image, ImageTk
from io import BytesIO
from openai import OpenAI

# ---------------- CONFIG ---------------- #

URL_BASE = "https://api.enem.dev/v1/exams"

questao_atual = {}

# IA LOCAL (LM STUDIO)
client_openAI = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

# ---------------- IA ---------------- #

def explicar_com_ia(resposta_usuario):
    try:

        loading = tk.Toplevel(janela)
        loading.title("IA")
        loading.geometry("300x100")
        loading.config(bg="#1e1e1e")

        texto_loading = tk.Label(
            loading,
            text="IA pensando...",
            font=("Arial", 14),
            fg="white",
            bg="#1e1e1e"
        )

        texto_loading.pack(expand=True)

        response = client_openAI.chat.completions.create(
            model="google/gemma-3-1b",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um professor didático do ENEM"
                },
                {
                    "role": "user",
                    "content": f"""
                    Observe essa questão do ENEM:

                    Matéria: {questao_atual['discipline']}

                    {questao_atual['title']}

                    {questao_atual['context']}

                    Alternativas:
                    {questao_atual['alternatives']}

                    Alternativa correta:
                    {questao_atual['correctAlternative']}

                    Alternativa escolhida:
                    {resposta_usuario}

                    Explique por que a alternativa escolhida está errada
                    e por que a correta está certa.
                    """
                }
            ],
            temperature=0.7
        )

        explicacao = response.choices[0].message.content

        loading.destroy()

        janela_exp = tk.Toplevel(janela)
        janela_exp.title("Explicação IA")
        janela_exp.geometry("900x600")
        janela_exp.config(bg="#1e1e1e")

        titulo = tk.Label(
            janela_exp,
            text="Explicação da IA",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e1e1e"
        )

        titulo.pack(pady=10)

        texto = tk.Text(
            janela_exp,
            wrap="word",
            font=("Arial", 12),
            bg="#252525",
            fg="white",
            insertbackground="white",
            padx=15,
            pady=15
        )

        texto.pack(fill="both", expand=True, padx=20, pady=20)

        texto.insert("1.0", explicacao)

        texto.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Erro IA", str(e))


# ---------------- QUIZ ---------------- #

def verificar_resposta(letra):

    correta = questao_atual["correctAlternative"]

    if letra.lower() == correta.lower():

        messagebox.showinfo(
            "Resultado",
            "⭐ Você acertou!"
        )

    else:

        resposta = messagebox.askyesno(
            "Resposta errada",
            f"❌ Errou faz enem!\n\nResposta correta: {correta}\n\nDeseja explicação da IA?"
        )

        if resposta:

            threading.Thread(
                target=explicar_com_ia,
                args=(letra,),
                daemon=True
            ).start()


def gerar_questao(dificuldade):

    global questao_atual

    ano = random.randint(2009, 2023)
    numero = random.randint(1, 180)

    url_api = f"{URL_BASE}/{ano}/questions/{numero}"

    try:

        response = requests.get(url_api)

        if response.status_code == 200:

            questao = response.json()
            questao_atual = questao

            titulo_label.config(
                text=f"ENEM {ano} - {questao['discipline'].capitalize()}"
            )

            texto = f"{questao['title']}\n\n{questao['context']}"

            pergunta_label.config(text=texto)

            # LIMPA BOTÕES
            for widget in frame_alternativas.winfo_children():
                widget.destroy()

            # ---------------- ALTERNATIVAS ---------------- #

            alternativas_completas = questao["alternatives"]

            correta = questao["correctAlternative"]

            alt_correta = None

            for alt in alternativas_completas:

                if alt["letter"].lower() == correta.lower():

                    alt_correta = alt
                    break

            alternativas_erradas = [

                alt for alt in alternativas_completas

                if alt["letter"].lower() != correta.lower()

            ]

            # DIFICULDADE

            if dificuldade == "Fácil":
                qtd = 3

            elif dificuldade == "Médio":
                qtd = 4

            else:
                qtd = 5

            random.shuffle(alternativas_erradas)

            alternativas = [alt_correta] + alternativas_erradas[:qtd - 1]

            random.shuffle(alternativas)

            # ---------------- BOTÕES ---------------- #

            for alt in alternativas:

                texto_alt = f"{alt['letter']}) {alt['text']}"

                btn = tk.Button(
                    frame_alternativas,
                    text=texto_alt,
                    wraplength=350,
                    justify="left",
                    anchor="w",
                    font=("Arial", 11),
                    bg="#2b2b2b",
                    fg="white",
                    activebackground="#444",
                    activeforeground="white",
                    padx=10,
                    pady=10,
                    command=lambda l=alt['letter']: verificar_resposta(l)
                )

                btn.pack(fill="x", pady=5)

            # ---------------- IMAGEM ---------------- #

            if questao.get("files"):

                try:

                    img_url = questao["files"][0]

                    img_res = requests.get(img_url)

                    img = Image.open(BytesIO(img_res.content))

                    img.thumbnail((350, 350))

                    img_tk = ImageTk.PhotoImage(img)

                    imagem_label.config(image=img_tk)

                    imagem_label.image = img_tk

                except:

                    imagem_label.config(image="")

            else:

                imagem_label.config(image="")

    except Exception as e:

        messagebox.showerror("Erro", str(e))


def abrir_quiz(dificuldade):

    tela_inicio.pack_forget()

    tela_quiz.pack(fill="both", expand=True)

    gerar_questao(dificuldade)

    botao_gerar.config(
        command=lambda: gerar_questao(dificuldade)
    )


# ---------------- JANELA ---------------- #

janela = tk.Tk()

janela.title("Quiz ENEM IA")

janela.geometry("1400x800")

janela.config(bg="#1e1e1e")

# ---------------- TELA INICIAL ---------------- #

tela_inicio = tk.Frame(
    janela,
    bg="#1e1e1e"
)

tela_inicio.pack(fill="both", expand=True)

# LOGO

try:

    url_logo = "https://vetores.org/wp-content/uploads/enem.png"

    img_res = requests.get(url_logo)

    img = Image.open(BytesIO(img_res.content))

    img = img.resize((300, 150))

    logo = ImageTk.PhotoImage(img)

    logo_label = tk.Label(
        tela_inicio,
        image=logo,
        bg="#1e1e1e"
    )

    logo_label.pack(pady=20)

except:
    pass

titulo = tk.Label(
    tela_inicio,
    text="QUIZ ENEM",
    font=("Arial", 30, "bold"),
    fg="white",
    bg="#1e1e1e"
)

titulo.pack(pady=10)

subtitulo = tk.Label(
    tela_inicio,
    text="Selecione a dificuldade",
    font=("Arial", 16),
    fg="white",
    bg="#1e1e1e"
)

subtitulo.pack(pady=10)

# BOTÕES

btn_facil = tk.Button(
    tela_inicio,
    text="Fácil",
    width=20,
    height=2,
    font=("Arial", 14),
    bg="green",
    fg="white",
    command=lambda: abrir_quiz("Fácil")
)

btn_facil.pack(pady=10)

btn_medio = tk.Button(
    tela_inicio,
    text="Médio",
    width=20,
    height=2,
    font=("Arial", 14),
    bg="orange",
    fg="white",
    command=lambda: abrir_quiz("Médio")
)

btn_medio.pack(pady=10)

btn_dificil = tk.Button(
    tela_inicio,
    text="Difícil",
    width=20,
    height=2,
    font=("Arial", 14),
    bg="red",
    fg="white",
    command=lambda: abrir_quiz("Difícil")
)

btn_dificil.pack(pady=10)

# ---------------- TELA QUIZ ---------------- #

tela_quiz = tk.Frame(
    janela,
    bg="#1e1e1e"
)

titulo_label = tk.Label(
    tela_quiz,
    text="",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#1e1e1e"
)

titulo_label.pack(pady=10)

# CONTAINER

container = tk.Frame(
    tela_quiz,
    bg="#1e1e1e"
)

container.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# ESQUERDA -> QUESTÃO

frame_pergunta = tk.Frame(
    container,
    bg="#252525",
    width=500
)

frame_pergunta.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)

pergunta_label = tk.Label(
    frame_pergunta,
    text="",
    wraplength=450,
    justify="left",
    anchor="nw",
    font=("Arial", 12),
    fg="white",
    bg="#252525",
    padx=15,
    pady=15
)

pergunta_label.pack(
    fill="both",
    expand=True
)

# MEIO -> IMAGEM

frame_imagem = tk.Frame(
    container,
    bg="#1e1e1e",
    width=400
)

frame_imagem.pack(
    side="left",
    fill="both",
    padx=10
)

imagem_label = tk.Label(
    frame_imagem,
    bg="#1e1e1e"
)

imagem_label.pack(expand=True)

# DIREITA -> ALTERNATIVAS

frame_alternativas = tk.Frame(
    container,
    bg="#252525",
    width=450
)

frame_alternativas.pack(
    side="right",
    fill="y",
    padx=10
)

# BOTÃO GERAR

botao_gerar = tk.Button(
    tela_quiz,
    text="Gerar Nova Questão",
    font=("Arial", 14),
    bg="#007acc",
    fg="white",
    padx=20,
    pady=10
)

botao_gerar.pack(pady=20)

# ---------------- LOOP ---------------- #

janela.mainloop()
