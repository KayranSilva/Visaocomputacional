import cv2
import matplotlib.pyplot as plt

def visualizar_hsv(img_bgr):
    # Converte a imagem de BGR para HSV
    hsv_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    rgb_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Divide os canais H, S e V
    h, s, v = cv2.split(hsv_img)

    # Cria uma figura com 4 subplots
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(rgb_img)
    axes[0].set_title('Imagem Original')
    axes[1].imshow(h, cmap='hsv')
    axes[1].set_title('Canal H (Hue)')
    axes[2].imshow(s, cmap='gray')
    axes[2].set_title('Canal S (Saturation)')
    axes[3].imshow(v, cmap='gray')
    axes[3].set_title('Canal V (Value)')
    for ax in axes:
        ax.axis('off')
    plt.tight_layout()
    plt.show()

imagemColor = cv2.imread('/home/aluno/Documents/kayran/bernie-almanzar.png', cv2.IMREAD_COLOR)
if imagemColor is None:
    raise FileNotFoundError('Imagem não encontrada: /home/aluno/Documents/kayran/bernie-almanzar.png')

visualizar_hsv(imagemColor)