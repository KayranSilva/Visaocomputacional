Scaling.py
from PIL import Image
import numpy as np

# 1. Carrgar a imagem e transformar em array Numpy
caminho_entrada = r"/home/aluno/Documents/kayran/tensor.jpeg"
imagem = Image.open(caminho_entrada).convert("RGB")  # Converte para RGB, descartando o canal alfa se houver
arr = np.array(imagem)
# largura, 3)

altura_orig, largura_orig = arr.shape[:2]  # altura e largura originais da imagem
print(f"Dimensões originais da imagem: {altura_orig}x{largura_orig} px " f"(shape Numpy: {arr.shape})")

# 2. Definir o novo tamanho da imagem em pixels(largura e altura)
nova_largura = 800  # largura desejada em pixels
nova_altura = 600  # altura desejada em pixels

# 3. Redimensionar em Numpy usando vizinho mais próximo (nearest neighbor)
# para cada pixel novo, calcula qual pixel da imagem original ele corresponde
linhas = (np.arange(nova_altura) * altura_orig / nova_altura).astype(int)
colunas = (np.arange(nova_largura) * largura_orig / nova_largura).astype(int)
arr_redimensionado = arr[linhas[:, None], colunas]
# shape: (nova_altura, nova_largura, 3)

# 4.Voltar paraimagem PIL só para salvar em disco
caminho_saida = r"/home/aluno/Documents/kayran/tensor_redimensionado.jpeg"
Image.fromarray(arr_redimensionado).save(caminho_saida)

print(f"Redimensionado: {nova_altura}x{nova_largura} px (shape Numpy: {arr_redimensionado.shape})")
print(f"Imagem redimensionada salva com sucesso!")