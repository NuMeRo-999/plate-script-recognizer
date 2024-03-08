import cv2
import numpy as np
import pytesseract
from collections import Counter
import re

# Configuración de pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar filtro Gaussiano para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Realizar la detección de bordes mediante Canny
    edges = cv2.Canny(blurred, 50, 150)
    
    return edges

def find_license_plate_contours(edges):
    # Encontrar los contornos en la imagen
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar los contornos que puedan representar matrículas
    possible_plates = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4 and cv2.contourArea(contour) > 1000:
            possible_plates.append(approx)
    
    return possible_plates

def recognize_license_plate(image, possible_plates):
    # Si se encontraron posibles matrículas
    if possible_plates:
        # Obtener el texto de todas las posibles matrículas
        plate_texts = []
        for plate in possible_plates:
            # Obtener las coordenadas de la matrícula
            x, y, w, h = cv2.boundingRect(plate)
            # Extraer la región de interés (ROI) que contiene la matrícula
            roi = image[y:y+h, x:x+w]
            # Utilizar pytesseract para reconocer el texto en la matrícula
            plate_text = pytesseract.image_to_string(roi, config='--psm 8')
            # Si se detectó texto, agregarlo a la lista
            if plate_text:
                plate_texts.append(plate_text.strip())
          
        # Si se detectó al menos una matrícula
        if plate_texts:
            # Contar las ocurrencias de cada texto de matrícula
            plate_counter = Counter(plate_texts)
            # Obtener el texto de matrícula más común (el que más se repite)
            most_common_plate_text = plate_counter.most_common(1)[0][0]
            
            # Dibujar un rectángulo y mostrar el texto para el resultado más común
            for plate in possible_plates:
                x, y, w, h = cv2.boundingRect(plate)
                roi = image[y:y+h, x:x+w]
                plate_text = pytesseract.image_to_string(roi, config='--psm 8')
                if plate_text.strip() == most_common_plate_text:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cleaned_text = clean_plate_text(most_common_plate_text)
                    cv2.putText(image, cleaned_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    print("Matrícula detectada:", cleaned_text)
                    break  # Solo procesamos la matrícula más común
    return image

def clean_plate_text(plate_text):
    # Patrón de caracteres no deseados
    pattern = r'[)\]|},.;]'
    # Reemplazar los caracteres no deseados por una cadena vacía
    cleaned_text = re.sub(pattern, '', plate_text)
    # Eliminar el primer caracter solo si la longitud del texto es mayor a 7
    if len(cleaned_text) > 7:
        cleaned_text = cleaned_text[1:]
    return cleaned_text

# Iniciar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocesar la imagen para detección de bordes
    edges = preprocess_image(frame)
    
    # Encontrar posibles matrículas
    possible_plates = find_license_plate_contours(edges)
    
    # Realizar el reconocimiento de matrículas
    frame_with_plate = recognize_license_plate(frame, possible_plates)
    
    # Mostrar el resultado
    cv2.imshow('License Plate Recognition', frame_with_plate)
    
    # Salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
