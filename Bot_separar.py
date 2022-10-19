import cv2
import os
import sys
import glob
import numpy as np

arquivos = glob.glob(r'../HashTag_Reconhecimento_CAPTCHA/img/destino/*')
# The above code is doing the following:
for arquivo in arquivos:
   # tratamento da imagem
    # Converting the image to grayscale and then inverting the colors.
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
    _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)

    # contorno de cada letra
    # Finding the contours of the image.
    contornos, _ = cv2.findContours(
        nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regiao_letras = []

    # Filtering the contours.
    # filtrar os contornos
    for contorno in contornos:
        (x, y, largura, altura) = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)
        if area > 20:
            regiao_letras.append((x, y, largura, altura))

    # Desenhar os contronos e separar letras
    # Drawing the contours and separating the letters.
    imagem_final = cv2.merge([imagem] * 3)
    i = 1
    for retangulo in regiao_letras:
        x, y, largura, altura = retangulo
        imagem_letra = imagem[y-2:y+altura+2, x-2:x +largura+2]  # colocando margem no retangulo
        i = i+1

        nome_arquivo = os.path.basename(
            arquivo).replace(".png", f"letra_{i}.png")
        try:
            cv2.imwrite(
                f"../HashTag_Reconhecimento_CAPTCHA/img/letras/{nome_arquivo}", imagem_letra)
        except:
            continue
        cv2.rectangle(imagem_final, (x-2, y-2),
                      (x+largura+2, y+altura+2), (0, 255, 0), (1))

    nome_arquivo = os.path.basename(arquivo)
    cv2.imwrite(
        f"../HashTag_Reconhecimento_CAPTCHA/img/identificado/{nome_arquivo}", imagem_final)
