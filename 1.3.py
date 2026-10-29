import cv2
import matplotlib.pyplot as plt

imagemColor = cv2.imread("imagens/coresai.jpeg")

cv2.imshow("Tó pa tu", imagemColor)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_rgb  =  cv2.imread("imagens/coresai.jpeg", cv2.COLOR_BGR2RGB)

plt .imshow(img_rgb)
plt.axis("off")
plt.show()
