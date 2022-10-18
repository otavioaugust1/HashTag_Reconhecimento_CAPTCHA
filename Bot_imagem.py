import cv2
import os
import glob

def tratar_imagens(pasta_origem, pasta_destino='../HashTag_Reconhecimento_CAPTCHA/img/destino/'):
    arquivos = glob.glob(f"{pasta_origem}/*")
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo)  # Coletar imagem
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY) # imagem em cinza        
        _, imagem_tratada = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY) #realizar tratamento        
        nome_arquivo = os.path.basename(arquivo) #nome do arquivo
        cv2.imwrite(f'{pasta_destino}/{nome_arquivo}',imagem_tratada) #salvando o arquivo  

if __name__ == "__main__":
    tratar_imagens('../HashTag_Reconhecimento_CAPTCHA/img/origem')