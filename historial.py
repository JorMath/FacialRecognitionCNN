import cv2
import face_recognition
import datetime
import time

# Imagen a comparar
image = cv2.imread("Images/jorman.jpg")
face_loc = face_recognition.face_locations(image)[0]
face_image_encodings = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0]

# Función para guardar en un archivo de texto
def guardar_registro(nombre):
    now = datetime.datetime.now()
    with open("registros.txt", "a") as file:
        file.write(f"{nombre} reconocido en {now.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Video Streaming
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
start_time = time.time()
while True:
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.flip(frame, 1)
    if time.time() - start_time >= 5:
        start_time = time.time()
        face_locations = face_recognition.face_locations(frame, model="cnn")
        if face_locations != []:
            for face_location in face_locations:
                face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
                result = face_recognition.compare_faces([face_image_encodings], face_frame_encodings)
                if result[0] == True:
                    text = "Jorman"
                    color = (125, 220, 0)
                    guardar_registro(text)  # Guardar registro en archivo
                else:
                    text = "Desconocido"
                    color = (50, 50, 255)
                cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
                cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
                cv2.putText(frame, text, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()
