import cv2
import face_recognition
import time
from datetime import datetime
import threading
import os

# Función para cargar las imágenes de referencia y obtener sus codificaciones faciales
def load_reference_images():
    reference_images = {}
    path = "Images/"
    for filename in os.listdir(path):
        name = os.path.splitext(filename)[0]
        image = cv2.imread(os.path.join(path, filename))
        face_loc = face_recognition.face_locations(image)[0]
        face_encoding = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0]
        reference_images[name] = (face_encoding, face_loc)
    return reference_images

# Crear una lista para almacenar el historial de personas reconocidas junto con la fecha y hora
recognized_history = []

# Función para exportar el historial cada 5 segundos
def export_history():
    while True:
        with open("registros.txt", "w") as file:
            for item in recognized_history:
                file.write("%s - %s\n" % (item[1], item[0]))
        print("Historial exportado a registros.txt")
        time.sleep(5)

# Iniciar el hilo para la exportación del historial
export_thread = threading.Thread(target=export_history)
export_thread.start()

# Cargar las imágenes de referencia y obtener sus codificaciones faciales
reference_images = load_reference_images()

# Video Streaming
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        for face_location in face_locations:
            face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]

            recognized_person = "Desconocido"
            for name, (reference_encoding, reference_loc) in reference_images.items():
                result = face_recognition.compare_faces([face_frame_encodings], reference_encoding)
                if result[0]:
                    recognized_person = name
                    break

            color = (50, 50, 255) if recognized_person == "Desconocido" else (125, 228, 0)
            cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
            cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
            cv2.putText(frame, recognized_person, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)

            # Agregar la persona reconocida al historial junto con la fecha y hora
            recognized_history.append((recognized_person, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()
