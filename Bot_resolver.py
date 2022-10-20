

import numpy as np
import os
import cv2
import pickle
from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
from Bot_imagem import tratar_imagens 


def quebrar_captcha():
# importar o modelo que a gente treinou e importar o tradutor
    with open("rotulos_model.dat","rb") as arquivo_tradutor:
        lb = pickle.load(arquivo_tradutor)

    modelo = load_model("IA_CAPTCHA.hdf5")

# usar o modelo para resolver os captchas (colocando em uma pasta resolver)
# tratar a imagem
    tratar_imagens("../HashTag_Reconhecimento_CAPTCHA/img/resolver", pasta_destino="../HashTag_Reconhecimento_CAPTCHA/img/resolver")
# identificar as letras
    arquivos = list(paths.list_images("../HashTag_Reconhecimento_CAPTCHA/img/resolver"))

    for arquivo in arquivos:
# tratamento da imagem    
        imagem = cv2.imread(arquivo)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)

# contorno de cada letra    
        contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        regiao_letras = []
 
# filtrar os contornos
        for contorno in contornos:
            (x, y, largura, altura) = cv2.boundingRect(contorno)
            area = cv2.contourArea(contorno)
            if area > 20:
                regiao_letras.append((x, y, largura, altura))

        regiao_letras = sorted(regiao_letras, key=lambda x: x[0])  # pode ser "key=lambda lista: lista[0]"
# desenhar os contronos e separar letras   
        imagem_final = cv2.merge([imagem] * 3)
        previsao = []

        i = 1
        for retangulo in regiao_letras:
            x, y, largura, altura = retangulo
            imagem_letra = imagem[y-2:y+altura+2, x-2:x +largura+2]  # colocando margem no retangulo
            
# dar a letra para AI decobrir a letra
            imagem_letra = resize_to_fit(imagem_letra, 20, 20)

# tratamento para o Keras funcionar
            imagem_letra = np.expand_dims(imagem_letra, axis=2)
            imagem_letra = np.expand_dims(imagem_letra, axis=0)

#prever a letras
            letra_prevista = modelo.predict(imagem_letra)
            letra_prevista = lb.inverse_transform(letra_prevista)[0]
            previsao.append(letra_prevista)

# desenhar a letra previsa na imagem_final (linha abaixo opcional)
          #  cv2.rectangle(imagem_final, (x-2, y-2),(x+largura+2, y+altura+2), (0, 255, 0), (1))

        texto_previsao = "".join(previsao).replace("_","")  
        print(texto_previsao)
        return texto_previsao 


if __name__ == "__main__":
    quebrar_captcha()







