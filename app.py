import cv2


# ler a imagem
img = cv2.imread('carros/placa1.jpg')

# transformar os canais RGB da imagem pra escala de CINZA
gray =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# limiarizar a imagem (colocar ela numa escalar bicolor)
ret, bin = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)

# desfocar a imagem para tirar "ruidos" da binarização
desfocar = cv2.GaussianBlur(bin, (5,5), 0)

# buscar contorno da placa
imgg, contorno, hierarquia = cv2.findContours(desfocar, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# selecionar contornos retangulares
for c in contorno:
    # contorno fechado
    perimetro = cv2.arcLength(c, True) 

    # eliminar sujeita
    if perimetro > 100:
        # aproximar a forma do contorno para um poligono parecido
        vertices = cv2.approxPolyDP(c, 00.3 * perimetro, True)

        # se tiver 4 vertices 
        if len(vertices) == 4:
            (x, y, alt, lar) = cv2.boudingRect(c)
            cv2.rectangle(img, (x,y), (x+alt, y+lar), (0,255,0), 2)
            # recorto a placa
            pontos = img[y:y + lar, x:x + alt]
            # salvo o recorte da placa numa outra pasta
            cv2.imwrite('cortada/corte.jgp', pontos)


# focar nos contornos (pintando-os)
# cv2.drawContours(img, contorno, -1, (0, 255, 0), 2)

cv2.imshow('bin', bin)



# cv2.waitKey(0)
# cv2.destroyAllWindows()