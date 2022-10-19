
#import pip
#pip.main(["install","imutils","tensorflow","numpy","sklearn","keras","keras.models"])

import cv2
import os
import numpy as np
import pickle
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from helpers import resize_to_fit  # padronizar o tamanho das imagens


dados = []
rotulos = []
pasta_base_imagens = "../HashTag_Reconhecimento_CAPTCHA/img/base_letras"
imagens = paths.list_images(pasta_base_imagens)

for arquivo in imagens:    
    rotulo = arquivo.split(os.path.sep)[-2]
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    # Paronizar as letras em 15px 15px
    imagem = resize_to_fit(imagem, 20, 20)
    
    # Adicionar dimensão para keras ler imagem
    imagem = np.expand_dims(imagem, axis=2)
    
    # Adicionar as listas de dados
    rotulos.append(rotulo)
    dados.append(imagem)

dados = np.array(dados, dtype="float")/255  # padronização dos dados
rotulos = np.array(rotulos)

# separar dados de treino(75%) e de teste(25%) --> X=dados, Y=rotulos
(X_train, X_teste, Y_train, Y_teste) = train_test_split(
    dados, rotulos, test_size=0.25, random_state=0)


# Converter Letras em Numeros da lista rotulos (utilizando o one-hot endodig)
lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_teste = lb.transform(Y_teste)

# Salvar o Arquivo do labelBinarizer com o pickle
with open('rotulos_model.dat', 'wb') as arquivo_pickle:
    pickle.dump(lb, arquivo_pickle)

# Criar e treinar a I.A
modelo = Sequential()

# Criando Camadas Neuronios

# Primeira Camada
modelo.add(Conv2D(20, (5, 5), padding="same",
           input_shape=(20, 20, 1), activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Segunda Camada
modelo.add(Conv2D(50, (5, 5), padding="same",
           input_shape=(20, 20, 1), activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Terceira Camada
modelo.add(Flatten())
modelo.add(Dense(500, activation="relu"))  # 500 --> numero de nós

# Camada de Saida
# 58--> Numero de saidas, de acordo com as letras e numeros
modelo.add(Dense(58, activation="softmax"))

# Compilar todas as Camadas:
modelo.compile(loss="categorical_crossentropy",
               optimizer="adam", metrics=["accuracy"])

# Treinas I.A
# batch_size --> Numero de saida dos neuronios
# epochs --> numero de tentativas de treinos
# verbose --> 0(não apresenta nda) 1(Barra de progresso)
modelo.fit(X_train, Y_train, validation_data=(
    X_teste, Y_teste), batch_size=58, epochs=10, verbose=1)

# Salvar o Modelo Treinado
modelo.save("IA_CAPTCHA.dat")
