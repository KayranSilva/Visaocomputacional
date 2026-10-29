import os

import cv2
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def ajustar_brilho_contraste(img, alpha=1.0, beta=0):
    """
    Ajusta o brilho e contraste de uma imagem.

    :param img: Imagem de entrada (BGR).
    :param alpha: Fator de contraste (1.0 mantém o contraste original).
    :param beta: Valor de brilho (0 mantém o brilho original).
    :return: Imagem ajustada.
    """
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)


def redimensionar(img, largura=None, altura=None, escala=None):
    """
    Redimensiona uma imagem para as dimensões especificadas.

    :param img: Imagem de entrada.
    :param largura: Nova largura da imagem.
    :param altura: Nova altura da imagem.
    :param escala: Escala da imagem (ex.: 0.5 para reduzir pela metade).
    :return: Imagem redimensionada.
    """
    if escala is not None:
        nova_largura = int(img.shape[1] * escala)
        nova_altura = int(img.shape[0] * escala)
    elif largura is not None and altura is not None:
        nova_largura, nova_altura = largura, altura
    elif largura is not None:
        nova_largura = largura
        proporcao = img.shape[0] / img.shape[1]
        nova_altura = max(1, int(nova_largura * proporcao))
    elif altura is not None:
        nova_altura = altura
        proporcao = img.shape[1] / img.shape[0]
        nova_largura = max(1, int(nova_altura * proporcao))
    else:
        raise ValueError("Você deve fornecer largura, altura ou uma escala.")

    interpolacao = (
        cv2.INTER_AREA
        if nova_largura < img.shape[1] and nova_altura < img.shape[0]
        else cv2.INTER_LINEAR
    )
    return cv2.resize(img, (nova_largura, nova_altura), interpolation=interpolacao)


def cortar(img, x, y, largura, altura):
    """
    Corta uma região da imagem.

    :param img: Imagem de entrada.
    :param x: Coordenada x do canto superior esquerdo do retângulo de corte.
    :param y: Coordenada y do canto superior esquerdo do retângulo de corte.
    :param largura: Largura do retângulo de corte.
    :param altura: Altura do retângulo de corte.
    :return: Imagem cortada.
    """
    return img[y:y + altura, x:x + largura]

def rotacionar(img, angulo, centro=None, escala=1.0):
    """
    Rotaciona a imagem em torno de um ponto central.

    :param img: Imagem de entrada.
    :param angulo: Ângulo de rotação em graus (positivo no sentido anti-horário).
    :param centro: Ponto central de rotação (x, y). Se None, usa o centro da imagem.
    :param escala: Fator de escala da imagem.
    :return: Imagem rotacionada.
    """
    (h, w) = img.shape[:2]
    if centro is None:
        centro = (w // 2, h // 2)

    matriz_rotacao = cv2.getRotationMatrix2D(centro, angulo, escala)
    return cv2.warpAffine(img, matriz_rotacao, (w, h))

imagem = cv2.imread('/home/aluno/Documents/kayran/bernie-almanzar.png')

imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
imagem_ajustada = ajustar_brilho_contraste(imagem_rgb, alpha=1.5, beta=30)
imagem_redimensionada = redimensionar(imagem_ajustada, escala=0.5)
imagem_cortada = cortar(imagem_redimensionada, 50, 50, 200, 200)
imagem_rotacionada = rotacionar(imagem_cortada, angulo=45)      

plt.figure(figsize=(16, 10))

plt.subplot(2, 3, 1)
plt.imshow(imagem_rgb)
plt.title('Imagem Original')
plt.axis('off')     

ax2 = plt.subplot(2, 3, 2)
plt.imshow(imagem_ajustada)
plt.title('Brilho e Contraste Ajustados')
plt.axis('off')

ax3 = plt.subplot(2, 3, 3)
plt.imshow(imagem_redimensionada)
plt.title('Imagem Redimensionada')      
ax3.axis('off') 

ax4 = plt.subplot(2, 3, 4) 
plt.imshow(imagem_cortada)
plt.title('Imagem Cortada')
ax4.axis('off')

ax5 = plt.subplot(2, 3, 5)
plt.imshow(imagem_rotacionada)
plt.title('Imagem Rotacionada')
ax5.axis('off')

plt.tight_layout()
saida = '/home/aluno/Documents/kayran/operacoes_basicas.png'
plt.savefig(saida, dpi=150)
print(f'Imagem salva em {saida}')

