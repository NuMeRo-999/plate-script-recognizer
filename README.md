**README - Sistema de Reconocimiento de Matrículas de Automóviles**

Este script implementa un sistema de reconocimiento de matrículas de automóviles utilizando la biblioteca OpenCV y Tesseract OCR (Optical Character Recognition). El sistema captura video desde una cámara en tiempo real, detecta posibles matrículas en los cuadros de video y utiliza Tesseract OCR para reconocer el texto de la matrícula.

### Requisitos
- Python 3.x
- [OpenCV](https://github.com/opencv/opencv-python) (`pip install opencv-python`)
- [Tesseract OCR](https://github.com/tesseract-ocr/tessdoc) (`pip install pytesseract`)
- Tesseract OCR debe estar instalado en el sistema.

### Ejecución
1. Clona o descarga este repositorio en tu máquina local.
2. Asegúrate de tener todos los requisitos mencionados anteriormente instalados.
3. Ejecuta el script `license_plate_recognition.py`.

```bash
python license_plate_recognition.py
```

4. La aplicación comenzará a capturar video desde la cámara. Coloca un automóvil frente a la cámara para que pueda detectar la matrícula.

### Uso
- Una vez que la aplicación esté en funcionamiento, mostrará el video en tiempo real de la cámara con las matrículas detectadas resaltadas y el texto de la matrícula reconocido impreso encima.
- Si se detecta una matrícula, se imprimirá el texto de la matrícula en la consola.

### Detalles de Implementación
- El script utiliza el algoritmo de Canny para detectar bordes en la imagen y encontrar regiones que puedan contener matrículas.
- Las regiones candidatas se filtran según su forma y tamaño para eliminar falsos positivos.
- Se utiliza Tesseract OCR para reconocer el texto de las matrículas.
- Se limpia el texto de la matrícula para eliminar caracteres no deseados y mejorar la precisión del reconocimiento.

### Personalización
- Si deseas cambiar la configuración de Tesseract OCR o ajustar los parámetros de detección de bordes, puedes modificar el código según tus necesidades.
- El script también puede modificarse para trabajar con videos pregrabados o imágenes estáticas en lugar de la entrada de la cámara en vivo.

### Notas
- La precisión del reconocimiento de matrículas puede variar según la calidad de la imagen de entrada y las condiciones de iluminación.
- Asegúrate de que la cámara esté correctamente configurada y enfocada para obtener mejores resultados de detección y reconocimiento.

