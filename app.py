import cv2


# ler a imagem
img = cv2.imread('carros/placa1.jpg')

# transformar os canais RGB da imagem pra escala de CINZA
gray =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# limiarizar a imagem (colocar ela numa escalar bicolor)
ret, bin = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)

cv2.imshow('bin', bin)



cv2.waitKey(0)
cv2.destroyAllWindows()