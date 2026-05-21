# 🎓 Quiz ENEM com Inteligência Artificial Local

Este projeto consiste em um simulador de questões do ENEM que consome dados reais da **API ENEM dev** e integra um Modelo de Linguagem (LLM) local para atuar como um professor didático, explicando os erros cometidos pelo usuário.

O projeto possui duas versões independentes:
1. **Versão Terminal:** Uma interface em linha de comando leve e direta.
2. **Versão Desktop (GUI):** Uma interface gráfica moderna construída em `tkinter` com suporte a imagens e execução assíncrona (threading) para a IA.

---

## ✨ Funcionalidades

- **Questões Reais:** Sorteio aleatório de questões reais do ENEM (entre os anos de 2009 e 2023) consumindo a API pública.
- **Níveis de Dificuldade Dinâmicos:**
  - **Fácil:** Apenas 3 alternativas visíveis.
  - **Médio:** Apenas 4 alternativas visíveis.
  - **Difícil:** Todas as 5 alternativas originais da prova.
- **Suporte a Imagens:** Exibição automática de imagens associadas às questões (se houver).
- **Professor IA Integrado:** Caso erre a questão, você pode solicitar uma explicação detalhada e didática gerada por uma Inteligência Artificial rodando localmente na sua máquina.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter** (Interface Gráfica)
- **Requests** (Consumo da [API ENEM dev](https://api.enem.dev/))
- **Pillow (PIL)** (Processamento e exibição de imagens)
- **OpenAI Python SDK** (Para comunicação com a IA local)
- **LM Studio** (Para servir o modelo open-source localmente)

---

## 🚀 Pré-requisitos & Configuração da IA

Para que o recurso de explicação por Inteligência Artificial funcione, você precisa configurar um provedor de LLM local compatível com a API da OpenAI. O código vem configurado por padrão para o **LM Studio**.

1. Baixe e instale o [LM Studio](https://lmstudio.ai/).
2. Procure e faça o download do modelo solicitado no código: `google/gemma-3-1b` (ou altere a string do modelo no código para o de sua preferência).
3. Vá até a aba **Local Server** no LM Studio e clique em **Start Server**.
4. Garanta que a porta padrão seja `1234` (o endpoint utilizado é `http://127.0.0.1:1234/v1`).

---

## 📦 Instalação

1. Clone este repositório ou baixe os arquivos de código.
2. Instale as dependências necessárias utilizando o `pip`:

```bash
pip install requests pillow openai
