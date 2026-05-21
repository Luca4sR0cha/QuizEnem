import subprocess
import sys
import tkinter as tk
import socket
import json
import random
from io import BytesIO

def verificar_libs():
    for lib in ["requests", "Pillow"]:
        try:
            __import__(lib if lib != "Pillow" else "PIL")
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

verificar_libs()
import requests
from PIL import Image, ImageTk

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="white")
        self.pontos = 0
        self.ip_server = '10.110.72.37'
        self.tela_dificuldade()

    def tela_dificuldade(self):
        self.limpar()
        tk.Label(self.root, text="DESAFIO ENEM REDE", font=("Arial", 30, "bold"), bg="white").pack(pady=50)
        for texto, qtd, cor in [("Fácil (3 Opções)", 3, "#b3ffb3"), ("Médio (4 Opções)", 4, "#b3d9ff"), ("Difícil (5 Opções)", 5, "#ffb3b3")]:
            tk.Button(self.root, text=texto, bg=cor, font=("Arial", 15), width=25, command=lambda q=qtd: self.setup_jogo(q)).pack(pady=10)
        tk.Button(self.root, text="SAIR", command=self.root.destroy, bg="gray", fg="white").pack(pady=20)

    def setup_jogo(self, qtd):
        self.qtd_alts = qtd
        self.pontos = 0
        self.montar_interface()
        self.proxima_questao()

    def montar_interface(self):
        self.limpar()
        self.lbl_score = tk.Label(self.root, text=f"PONTOS: {self.pontos}", font=("Arial", 18, "bold"), bg="white", fg="blue")
        self.lbl_score.pack(pady=10)
        
        self.lbl_pergunta = tk.Label(self.root, text="", font=("Arial", 12, "bold"), bg="white", wraplength=1000, justify="center")
        self.lbl_pergunta.pack(pady=5)

        self.lbl_img = tk.Label(self.root, bg="white")
        self.lbl_img.pack()

        self.f_alts = tk.Frame(self.root, bg="white")
        self.f_alts.pack(pady=10)
        self.labels_txt = []
        for i in range(self.qtd_alts):
            l = tk.Label(self.f_alts, text="", font=("Arial", 10), bg="white", wraplength=850, width=110, anchor="w", justify="left")
            l.pack()
            self.labels_txt.append(l)

        self.f_btns = tk.Frame(self.root, bg="white")
        self.f_btns.pack(pady=15)
        self.btns = []
        for letra in "abcde"[:self.qtd_alts]:
            b = tk.Button(self.f_btns, text=letra.upper(), width=10, font=("Arial", 12, "bold"), command=lambda l=letra: self.validar(l))
            b.pack(side="left", padx=5)
            self.btns.append(b)

        self.btn_next = tk.Button(self.root, text="CARREGANDO...", state="disabled", command=self.proxima_questao, bg="#2ecc71", fg="white", width=25)
        self.btn_next.pack(side="bottom", pady=40)

    def proxima_questao(self):
        self.btn_next.config(text="BUSCANDO NO SERVIDOR...", state="disabled")
        self.root.update()
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip_server, 5000))
            s.send("GET".encode())
            raw = b""
            while True:
                part = s.recv(4096)
                if not part: break
                raw += part
            s.close()
            q = json.loads(raw.decode('utf-8'))
        except:
            self.lbl_pergunta.config(text="❌ ERRO DE CONEXÃO COM O SERVIDOR 10.110.72.37")
            return

        self.correta_real = q['correctAlternative'].lower()
        self.lbl_pergunta.config(text=f"ENEM {q['ano_sorteado']} - {q['discipline'].upper()}\n\n{q['title']}\n{q['context']}")
        
        # Imagem Redimensionada
        if q.get('files'):
            try:
                url = q['files'] if isinstance(q['files'], str) else q['files'][0]
                r = requests.get(url, timeout=5)
                img = Image.open(BytesIO(r.content))
                img.thumbnail((650, 450))
                tk_img = ImageTk.PhotoImage(img)
                self.lbl_img.config(image=tk_img, text="")
                self.lbl_img.image = tk_img
            except: self.lbl_img.config(image="", text="(Erro na imagem)")
        else: self.lbl_img.config(image="", text="")

        # Embaralhar alts mantendo a correta
        todas = q['alternatives']
        c_obj = next(a for a in todas if a['letter'].lower() == self.correta_real)
        erradas = random.sample([a for a in todas if a['letter'].lower() != self.correta_real], self.qtd_alts - 1)
        final = sorted(erradas + [c_obj], key=lambda x: x['letter'])

        for i in range(self.qtd_alts):
            letra_tela = "abcde"[i]
            if final[i]['letter'].lower() == self.correta_real: self.correta_atual = letra_tela
            self.labels_txt[i].config(text=f"{letra_tela.upper()}) {final[i]['text']}", bg="white")
            self.btns[i].config(state="normal", bg="SystemButtonFace")
        
        self.btn_next.config(text="PRÓXIMA PERGUNTA", state="disabled")

    def validar(self, escolha):
        if escolha == self.correta_atual:
            self.pontos += 10
            self.lbl_score.config(text=f"PONTOS: {self.pontos}")
        
        for i, b in enumerate(self.btns):
            letra = "abcde"[i]
            if letra == self.correta_atual: self.labels_txt[i].config(bg="#c3e6cb")
            elif letra == escolha: self.labels_txt[i].config(bg="#f5c6cb")
            b.config(state="disabled")
        self.btn_next.config(state="normal")

    def limpar(self):
        for w in self.root.winfo_children(): w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
