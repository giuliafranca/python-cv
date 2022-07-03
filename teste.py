from os import walk
import cv2
import pytesseract



def filtrar_placa(img):
    # ler a imagem (fazer na main)
    img = cv2.imread(img)
    cv2.imshow('imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # transformar os canais RGB da imagem pra escala de CINZA
    gray =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('cinza', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # limiarizar a imagem (colocar ela numa escalar bicolor)
    _, bines = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)
    cv2.imshow('binario', bines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # desfocar a imagem para tirar "ruidos" da binarização
    desfoque = cv2.GaussianBlur(bines,(7,7),0)
    cv2.imshow('desenho', desfoque)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # buscar contorno da placa
    contorno, _ = cv2.findContours(desfoque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(str(len(contorno)))

    img_contorno = img.copy()

    cv2.drawContours(img, contorno, -1, (0, 255, 0), 2)
    cv2.imshow('contornos', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    lista_contorno = []
    # selecionar contornos retangulares
    for c in contorno:
        # contorno fechado
        perimetro = cv2.arcLength(c, True) 
        # eliminar sujeita
        if perimetro > 160 and perimetro < 1800:
            # aproximar a forma do contorno para um poligono parecido
            vertices = cv2.approxPolyDP(c, 0.02 * perimetro, True)
                # se tiver 4 vertices 
            if len(vertices) == 4:
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(img_contorno, (x,y), (x+alt, y+lar), (0,255,0), 2)
                lista_contorno.append(c)
                print(str(len(lista_contorno)))
                # recorto a placa
                pontos = img_contorno[y:y + lar, x:x + alt]
                # salvo o recorte da placa numa outra pasta
                cv2.imwrite('cortada/pontos.jpg', pontos)         

    cv2.imshow('contornos', img_contorno)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def processar_placa():
    #tratar a imagem so da placa com foi feito com a imagem geral
    
    placa = cv2.imread("cortada/pontos.jpg")

    if placa is None:
        return 
    
    resize = cv2.resize(placa, None, fx=4, fy=4, interpolation = cv2.INTER_CUBIC)
    placa_cinza = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
    _, placa_limiarizada = cv2.threshold(placa_cinza, 50, 255, cv2.THRESH_BINARY)

    cv2.imwrite("tratada/placa.jpg", placa_limiarizada)

def acharsaida():
    placa = cv2.imread("tratada/placa.jpg")
    pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    saida = pytesseract.image_to_string(placa, lang="eng", config=config)
    return saida


if __name__ == "__main__":
    img = "carros/placa1.jpg"
    filtrar_placa(img)
    
    processar_placa()
    
    ocr = acharsaida()
    print(ocr)

    images = [
        'carros/placa1.jpg',
        'carros/placa2.jpg',
        'carros/placa3.jpg',
        'carros/placa4.jpg'
    ]

    _, _, fila = next(walk('carros/'))
    print(fila)





