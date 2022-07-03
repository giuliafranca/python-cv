import cv2

def filtrar_img(imagem):

    # ler a imagem (fazer na main)
    # img = cv2.imread('carros/placa3.jpg')

    # transformar os canais RGB da imagem pra escala de CINZA
    gray =  cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # limiarizar a imagem (colocar ela numa escalar bicolor)
    _, bines = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)

    # desfocar a imagem para tirar "ruidos" da binarização
    desfoque = cv2.GaussianBlur(bines,(5,5),0)
    return desfoque

def encontrar_contorno(desfoque):
    # buscar contorno da placa
    contorno, hierarquia = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contorno

def desenhar_contorno(contorno, imagem):
    # selecionar contornos retangulares
    for c in contorno:
        # contorno fechado
        perimetro = cv2.arcLength(c, True) 

        # eliminar sujeita
        if perimetro > 120:
            # aproximar a forma do contorno para um poligono parecido
            vertices = cv2.approxPolyDP(c, 00.3 * perimetro, True)

            # se tiver 4 vertices 
            if len(vertices) == 4:
                (x, y, alt, lar) = cv2.boudingRect(c)
                cv2.rectangle(imagem, (x,y), (x+alt, y+lar), (0,255,0), 2)
                # recorto a placa
                pontos = imagem[y:y + lar, x:x + alt]
                # salvo o recorte da placa numa outra pasta
                cv2.imwrite('cortada/pontos.jpg', pontos)
                        


# focar nos contornos (pintando-os)
# cv2.drawContours(img, contorno, -1, (0, 255, 0), 2)

# cv2.imshow('desenho', img)



