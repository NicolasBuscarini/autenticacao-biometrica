import cv2
import numpy as np
import fingerprint_enhancer

def AbrirImagem(image):
    imagem = cv2.imread(image, 0)
    cv2.imshow("Imagem Recebida", imagem)
    return imagem

def ErosaoDaImagem(image):
    imagem = cv2.imread(image, 0)
    elementoEstruturante = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE,	(2,2))
    imagemErosao = cv2.erode(
		imagem,	elementoEstruturante, iterations = 2
    )
    cv2.imshow("Erosão da Imagem", imagemErosao)

def AberturaDaImagem(image):
    imagem = cv2.imread(image, 0)
    elementoEstruturante = cv2.getStructuringElement(
		cv2.MORPH_ELLIPSE, (1,1)
    )
    imagemAbertura = cv2.morphologyEx(
    imagem, cv2.MORPH_OPEN, elementoEstruturante
    )
    cv2.imshow("Abertura de Imagem", imagemAbertura)

def DilatacaoDaImagem(image):
    imagem = cv2.imread(image, 0);
    elementoEstruturante = cv2.getStructuringElement(
		cv2.MORPH_ELLIPSE, (3,3)
    )
    imagem = cv2.dilate(
        imagem, elementoEstruturante, iterations=2
    )
    cv2.imshow("Dilatação da Imagem", imagem)

def FechamentoDaImagem(image):
    imagem = cv2.imread(image, 0);
    elementoEstruturante = cv2.getStructuringElement(
		cv2.MORPH_ELLIPSE, (3,3)
    )
    imagem = cv2.morphologyEx(
	imagem, cv2.MORPH_CLOSE,	elementoEstruturante
    )
    cv2.imshow("Fechamento da Abertura", imagem)
  
def Enhance(image):
    imagem	=	cv2.imread(image,	0)
    out = fingerprint_enhancer.enhance_Fingerprint(imagem)
    cv2.imshow("Enhance",	out)


Enhance('biometria.bmp')
cv2.waitKey(0)
cv2.destroyAllWindows()

Enhance('biometria.png')
cv2.waitKey(0)
cv2.destroyAllWindows()



