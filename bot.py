#Feito com carinho por Thiago Narcizo <3

import numpy as np
import streamlit as st
import cv2
from random import randint
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFont
from PIL import ImageDraw

st.set_page_config(
    page_icon='✍️',
    page_title='Adivinhe quem tuitou',
    layout='wide'
)


#cadeia de markov para gerar a frase:
pessoa = open(r'tweets.txt', encoding='utf8').read()
pessoa.replace(' q ', ' que ')
pessoa.replace('”', '')
pessoa.replace('“', '')
pessoa.replace('(', '')
pessoa.replace(')', '')

#separando as palavras:
split_pessoa = pessoa.split()

#gerando a lista de primeiras palavras:
primeiras_palavras = []

for line in pessoa.split('\n'):
    if line != '':
        primeiras_palavras.append(line.split()[0])

#função para gerar os pares de palavras:
def pares(split_pessoa):
    for i in range(len(split_pessoa)-1):
        yield (split_pessoa[i], split_pessoa[i+1])

#criando os pares de palavras:
pairs = pares(split_pessoa)

#criando o dicionário de palavras:
dict_palavras = {}

for word_1, word_2 in pairs:
    if word_1 in dict_palavras.keys():
        dict_palavras[word_1].append(word_2)
    else:
        dict_palavras[word_1] = [word_2]

#gerando a primeira palavra da frase:
primeira_palavra = np.random.choice(primeiras_palavras)
chain = [primeira_palavra]

#gerando o número de palavras da frase:
n_palavras = randint(10, 20)

#gerando a frase:
for i in range(n_palavras):
    try:
        chain.append(np.random.choice(dict_palavras[chain[-1]]))
    except KeyError:
        chain.append(np.random.choice(primeiras_palavras))

#filtrando a última palavra da frase:
if chain[-1] in ["que", "a", "o", "q", "e", "mas", "da", "de", "do", "em", "para", "com", "na", "no", "um", "uma", "se", "por", "como", "ao", "mais", "os", "as", "das", "dos", "nos", "nas", "pelo", "pelos", "pela", "pelas", "ou", "que", "quando", "onde", "qual", "quais", "quem", "seu", "sua", "seus", "suas", "ser", ",", "meu", "seu", "sua", "é"]:
    chain.pop()

frase = ' '.join(chain)

#---------------------------------------------------------------------------------
#gerando imagem do tweet:
top_img = cv2.imread('imgs/top.png')
top_img = cv2.cvtColor(top_img, cv2.COLOR_BGR2RGB)
bot_img = cv2.imread('imgs/bottom.png')

#criando uma imagem com texto
text_color = (255, 255, 255)
font_size = 30
font = ImageFont.truetype("arial.ttf", font_size)
_, _, text_width, text_height = font.getbbox(frase)
text_image = Image.new("RGB", (text_width, text_height), (0, 0, 0))
draw = ImageDraw.Draw(text_image)
text_position = (0, 0)
draw.text(text_position, frase, font=font, fill=text_color)

#redimensionando as imagens para o tamanho do texto gerado
original_height, original_width, _ = top_img.shape
new_width = text_width
new_height = int(original_height * (new_width / original_width))

top_img = cv2.resize(top_img, (new_width, new_height))
bot_img = cv2.resize(bot_img, (new_width, new_height))

blackbar1 = np.zeros((7, new_width, 3), np.uint8)

#combinando as imagens verticalmente
combined_image = np.vstack((top_img, text_image, blackbar1, bot_img))

#criando duas blackbars e adicionar ao lado da combined_image
blackbar = np.zeros((combined_image.shape[0], 10, 3), np.uint8)
combined_image = np.hstack((blackbar, combined_image, blackbar))

#---------------------------------------------------------------------------- ST:
st.title("Essa pessaoa tuitaria algo como:")

if st.button(r'$\textsf{\LARGE Gerar Tweet}$'):
    st.image(combined_image, use_column_width=True)
    #st.latex(r'\textsf{\LARGE '+frase+'}')

#apenas por questão de controle:
print(frase)