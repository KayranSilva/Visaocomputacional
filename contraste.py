import cv2
import matplotlib.pyplot as plt


def histograma_pb(img_gray):
    return cv2.calcHist([img_gray], [0], None, [256], [0, 256])


def histograma_rgb(img_rgb):
    return [cv2.calcHist([img_rgb], [i], None, [256], [0, 256]) for i in range(3)]


def clahe_pb(img_gray, clip_limit=2.0, title_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=title_size)
    return clahe.apply(img_gray)


def clahe_colorido(img_bgr, clip_limite=2.0, title_size=(8, 8)):
    return clahe_colorido_lab(img_bgr, clip_limite=clip_limite, title_size=title_size)


def clahe_colorido_lab(img_bgr, clip_limite=2.0, title_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limite, tileGridSize=title_size)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_corr = clahe.apply(l)
    lab_corr = cv2.merge((l_corr, a, b))
    return cv2.cvtColor(lab_corr, cv2.COLOR_LAB2BGR)


def clahe_coloridp(img_bgr, clip_limite=2.0, title_size=(8, 8)):
    return clahe_colorido_lab(img_bgr, clip_limite=clip_limite, title_size=title_size)


def plotar_comparacao_pb(imag_orig, img_corr):
    hist_orig = histograma_pb(imag_orig)
    hist_corr = histograma_pb(img_corr)

    plt.figure(figsize=(12, 10))

    ax1 = plt.subplot(2, 2, 1)
    ax1.imshow(imag_orig, cmap='gray')
    ax1.set_title('Original P&B')
    ax1.axis('off')

    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(hist_orig, color='black')
    ax2.fill_between(range(256), hist_orig.flatten(), alpha=0.3, color='gray')
    ax2.set_title('Histograma original P&B')
    ax2.set_xlabel('Intensidade de pixel')
    ax2.set_ylabel('Número de pixels')

    ax3 = plt.subplot(2, 2, 3)
    ax3.imshow(img_corr, cmap='gray')
    ax3.set_title('Imagem corrigida P&B')
    ax3.axis('off')

    ax4 = plt.subplot(2, 2, 4)
    ax4.plot(hist_corr, color='black')
    ax4.fill_between(range(256), hist_corr.flatten(), alpha=0.3, color='gray')
    ax4.set_title('Histograma corrigido P&B')
    ax4.set_xlabel('Intensidade de pixel')
    ax4.set_ylabel('Número de pixels')

    plt.tight_layout()
    plt.show()


def plotar_comparacao_rgb(imag_orig, img_corr):
    hist_orig = histograma_rgb(imag_orig)
    hist_corr = histograma_rgb(img_corr)

    rgb_orig = cv2.cvtColor(imag_orig, cv2.COLOR_BGR2RGB)
    rgb_corr = cv2.cvtColor(img_corr, cv2.COLOR_BGR2RGB)

    cores = ('red', 'green', 'blue')
    rotulos = ('Vermelho', 'Verde', 'Azul')

    plt.figure(figsize=(12, 10))

    ax1 = plt.subplot(2, 2, 1)
    ax1.imshow(rgb_orig)
    ax1.set_title('Original RGB')
    ax1.axis('off')

    ax2 = plt.subplot(2, 2, 2)
    for hist, cor, rotulo in zip(hist_orig, cores, rotulos):
        ax2.plot(hist, color=cor, label=rotulo)
    ax2.set_title('Histograma original RGB')
    ax2.set_xlabel('Intensidade de pixel')
    ax2.set_ylabel('Número de pixels')
    ax2.legend(loc='upper left', fontsize='small')

    ax3 = plt.subplot(2, 2, 3)
    ax3.imshow(rgb_corr)
    ax3.set_title('Imagem corrigida RGB')
    ax3.axis('off')

    ax4 = plt.subplot(2, 2, 4)
    for hist, cor, rotulo in zip(hist_corr, cores, rotulos):
        ax4.plot(hist, color=cor, label=rotulo)
    ax4.set_title('Histograma corrigido RGB')
    ax4.set_xlabel('Intensidade de pixel')
    ax4.set_ylabel('Número de pixels')
    ax4.legend(loc='upper right', fontsize='small')

    plt.tight_layout()
    plt.show()


def plotar_comparacao_colorida(imag_orig, img_corr):
    plotar_comparacao_pb(imag_orig, img_corr)


# Exemplo de uso (descomente quando quiser executar manualmente):
# image = cv2.imread('imagens/lenna.png')
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray_corr = clahe_pb(gray_image)
# plotar_comparacao_pb(gray_image, gray_corr)
# color_corr = clahe_colorido(image)
# plotar_comparacao_rgb(image, color_corr)

