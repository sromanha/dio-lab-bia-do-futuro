#carregar os dados
import json
import streamlit as st
import pandas as pd
import requests

#configurações
OLLAMA_URL = 'http://localhost:11434/api/v1/generate'
MODELO = "gpt-oss"

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

#montar contexto
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMONIO: R$ {perfil['patrimonio_total']:.2f} | RESERVA: R$ {perfil['reserva_emergencia_atual']:.2f}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES
{json.dumps(produtos, indent=2, ensure_ascii=False)}

"""

#system prompt
SYSTEM_PROMPT = """Você é o Edu, um educador financeiro amigável e didático.

OBJETIVO: Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos

REGRAS:
1. Nunca recomende investimentos específicos - apenas explique como eles funcionam
2. Use os dados fornecidos para dar exemplos personalizados
3. Use linguagem simples, como se explicasse para um amigo
4. Se não souber algo, admita: "Não tenho essa informação"
5. Sempre pergunte se o cliente entendeu
"""

#chamar ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}
    {contexto}

    PERGUNTA: {msg}""" 

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stram": False})
    return r.json()['response']

#interface
st.title("Edu - Seu Educador Financeiro")

if pergunta := st.text_input("Faça uma pergunta sobre finanças pessoais:"):
    st.chat.message("user").write(pergunta)
    with st.spinner("Pensando..."):
        st.chat.message("assistant").write(perguntar(pergunta)) 