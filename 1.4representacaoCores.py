import cv2
import matplotlib.pyplot as plt

# - Função Separar canais rgb

def separar_canais_rgb(img_brg):

    azul = img_brg[:,:,0]
    verde = img_brg[:,:, 1]
    vermelho = img_brg[:,:,2]

    return vermelho, verde, azul

def visualizar_canais(img_brg):

    img_brg = cv2.cvtColor(img_brg, cv2.COLOR_BGR2RGB)
    r, g, b = separar_canais_rgb(img_brg)

    fig, axs = plt.subplots(1, 4, figsize=(16, 4))

    axs[0].imshow(img_brg); axs[0].set_title('Imagem Original')
    axs[1].imshow(r, cmap='gray'); axs[1].set_title('Canal Vermelho')
    axs[2].imshow(g, cmap='gray'); axs[2].set_title('Canal Verde')
    axs[3].imshow(b, cmap='gray'); axs[3].set_title('Canal Azul')
    for ax in axs: 
        ax.axis('off')
        plt.tight_layout(); 
plt.show()

imagemcolor = cv2.imread('/home/aluno/Documents/kayran/bernie-alzamar.png', cv2.IMREAD_COLOR)
imagemBlack = cv2.imread('/home/aluno/Documents/kayran/bernie-alzamar.png', cv2.IMREAD_GRAYSCALE)

print("Conteudo numérico da imagem imagemBlack.png (em escala de cinza):")
print("Forma do vetor:", imagemBlack.shape)

print("primeiras 3x3 pixels da imagem (BRG):", imagemcolor[:3, :3, :])

imagemcolor = cv2.imread('/home/aluno/Documents/kayran/bernie-alzamar.png', cv2.IMREAD_COLOR)