import cv2
import matplotlib.pyplot as plt
import os
import zipfile

def salvar_jpeg(img_bgr, caminho, qualidade=95):
    cv2.imwrite(caminho, img_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), qualidade])

    parms = [int(cv2.IMWRITE_JPEG_QUALITY), qualidade]
    cv2.imwrite(caminho, img_bgr, parms)

def salvar_png(img_bgr, caminho, compressao=3):
    parms = [int(cv2.IMWRITE_PNG_COMPRESSION), compressao]
    cv2.imwrite(caminho, img_bgr, parms)

def tamanho_kb(caminho):
    return os.path.getsize(caminho) / 1024

def plotar_comparacao_tamanho_jpeg(img_bgr, pasta, qualidade=(10, 50, 75, 95)):
    os.makedirs(pasta, exist_ok=True)
    n = len(qualidade)

    plt.figure(figsize=(14 * n, 5))
    plt.suptitle("Comparação de tamanhos de arquivos JPEG", fontsize=14)

    for i, q in enumerate(qualidade):
        caminho = os.path.join(pasta, f"imagem_qualidade_{q:03d}.jpg")
        salvar_jpeg(img_bgr, caminho, qualidade=q)
        kb = tamanho_kb(caminho)

        ax = plt.subplot(1, n, i + 1)
        ax.imshow(cv2.cvtColor(cv2.imread(caminho), cv2.COLOR_BGR2RGB))
        ax.set_title(f"Qualidade {q}\n{kb:.1f} KB")
        ax.axis("off")
        plt.tight_layout()
        plt.show()

def plotar_comparacao_tamanho_png(img_bgr, pasta, compressao=(0, 3, 6, 9)):
    os.makedirs(pasta, exist_ok=True)
    n = len(compressao)

    plt.figure(figsize=(44 * n, 5))
    plt.suptitle("Comparação de tamanhos de arquivos PNG", fontsize=14)

    for i, c in enumerate(compressao):
        caminho = os.path.join(pasta, f"imagem_compressao_{c}.png")
        salvar_png(img_bgr, caminho, compressao=c);
        kb = tamanho_kb(caminho)

        ax = plt.subplot(1, n, i + 1)
        ax.imshow(cv2.cvtColor(cv2.imread(caminho), cv2.COLOR_BGR2RGB))
        ax.set_title(f"Compressão {c}\n{kb:.1f} KB")
        ax.axis("off")
        plt.tight_layout()
        plt.show()

def plotar_resumo_tamanhos(pasta, extensoes=(".jpg", ".png")):
    arquivos = [f for f in os.listdir(pasta) if f.endswith(extensoes)]
    key=lambda x:  os.path.getsize(os.path.join(pasta, x))
    tamanhos = [tamanho_kb(os.path.join(pasta, f)) for f in arquivos]
    
    nomes = [f.replace(extensoes[0], "").replace(extensoes[1], "") for f in arquivos]
    cores = ["steelblue" if f.endswith(".jpg") else "seagreen" for f in arquivos]

    plt.figure(figsize=(10, 5))
    barras = plt.bar(nomes, tamanhos, color=cores)
    plt.title("Comparação de tamanhos de arquivos")
    plt.xlabel("Arquivos")
    plt.ylabel("Tamanho (KB)")

    for barra, tamanho in zip(barras, tamanhos):
        plt.text(barra.get_width() / 2 + barra.get_x(), barra.get_y() + barra.get_height() + 1, f"{tamanho:.1f} KB", ha='center', fontdict=9)

        plt.tight_layout()
        plt.show()