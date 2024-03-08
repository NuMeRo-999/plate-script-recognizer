import cv2
import numpy as np
import pytesseract
from PIL import Image

# cap = cv2.VideoCapture('.mp4')  # Coloca la ruta de tu video aquí

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)  # 0 indica la primera cámara disponible en tu sistema

Ctexto = ''

while True:
    # Capturar el fotograma de la cámara
    ret, frame = cap.read()

    if ret == False:
        break

    # Dibujar un rectángulo
    cv2.rectangle(frame, (870, 750), (1070, 850), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, Ctexto[0:7], (900, 810), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    al, an, c = frame.shape

    x1 = int(an / 3)
    x2 = int(x1 * 2)

    y1 = int(al / 3)
    y2 = int(y1 * 2)

    cv2.rectangle(frame, (0,0), (400, 100), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, 'Procesando Placa', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    recorte = frame[y1:y2, x1:x2]

    mB = recorte[:, :, 0]
    mG = recorte[:, :, 1]
    mR = recorte[:, :, 2]
    Color = cv2.absdiff(mG, mB)

    _, umbral = cv2.threshold(Color, 40, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contornos = sorted(contornos, key=lambda x: cv2.contourArea(x), reverse=True)

    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if 500 < area < 5000:  # Filtrar por área
            x, y, ancho, alto = cv2.boundingRect(contorno)

            xpi = x + x1
            ypi = y + y1

            xpf = x + ancho + x1
            ypf = y + ancho + y1

            cv2.rectangle(frame, (xpi, ypi), (xpf, ypf), (255, 255, 255), 2)

            placa = frame[ypi:ypf, xpi:xpf]

            alp, anp, cp = placa.shape

            Mva = np.zeros((alp, anp))

            mBp = np.matrix(placa[:, :, 0])
            mGp = np.matrix(placa[:, :, 1])
            mRp = np.matrix(placa[:, :, 2])

            for col in range(0, alp):
                for fil in range(0, anp):
                    Max = max(mRp[col, fil], mGp[col, fil], mBp[col, fil])
                    Mva[fil, col] = 255 - Max

            # Binarizar la matrícula
            _, bin = cv2.threshold(Mva, 150, 255, cv2.THRESH_BINARY)

            bin = bin.reshape((alp, anp))
            bin = Image.fromarray(bin)
            bin = bin.convert('L')

            if alp >= 36 and anp >= 82:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

                config = '--psm 1'
                texto = pytesseract.image_to_string(bin, config=config)
                Ctexto = texto
                if len(texto) >= 3:
                    print(Ctexto)
                    break

        print(Ctexto)
    cv2.imshow('Vehiculos', frame)

    t = cv2.waitKey(1)

    if t == 27:
        break

# Liberar la captura de la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
