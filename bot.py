import numpy as np
import streamlit as st
from random import randint

pessoa = open(r'tweets.txt', encoding='utf8').read()
pessoa.replace(' q ', ' que ')
pessoa.replace('”', '')
pessoa.replace('“', '')
pessoa.replace('(', '')
pessoa.replace(')', '')

split_pessoa = pessoa.split()

primeiras_palavras = []

for line in pessoa.split('\n'):
    if line != '':
        primeiras_palavras.append(line.split()[0])

def pares(split_pessoa):
    for i in range(len(split_pessoa)-1):
        yield (split_pessoa[i], split_pessoa[i+1])

pairs = pares(split_pessoa)

dict_palavras = {}

for word_1, word_2 in pairs:
    if word_1 in dict_palavras.keys():
        dict_palavras[word_1].append(word_2)
    else:
        dict_palavras[word_1] = [word_2]


primeira_palavra = np.random.choice(primeiras_palavras)


chain = [primeira_palavra]

n_palavras = randint(5, 20)

for i in range(n_palavras):
    try:
        chain.append(np.random.choice(dict_palavras[chain[-1]]))
    except KeyError:
        chain.append(np.random.choice(primeiras_palavras))

if chain[-1] in ["que", "a", "o", "q", "e", "mas", "da", "de", "do", "em", "para", "com", "na", "no", "um", "uma", "se", "por", "como", "ao", "mais", "os", "as", "das", "dos", "nos", "nas", "pelo", "pelos", "pela", "pelas", "ou", "que", "quando", "onde", "qual", "quais", "quem", "seu", "sua", "seus", "suas", "ser", ",", "meu", "seu", "sua"]:
    chain.pop()

frase = ' '.join(chain)

#---------------------------------------------------------------------------- ST:

st.set_page_config(
    page_icon='✍️',
    page_title='Adivinhe quem tuitou',
    layout='wide'
)

st.title("Essa pessoa tuitaria algo como:")


if st.button(r'''$\textsf{\LARGE Gerar Tweet}$'''):
    st.latex(r'\textsf{\LARGE '+frase+'}')
