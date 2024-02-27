import cv2
import face_recognition
import time
from datetime import datetime
import threading


reference_image = cv2.imread("Images/jorman.jpg")
reference_face_loc = face_recognition.face_locations(reference_image)[0]
reference_face_encoding = face_recognition.face_encodings(reference_image, known_face_locations=[reference_face_loc])[0]

recognized_history = []

def export_history():
    while True:
        with open("registros.txt", "w") as file:
            for item in recognized_history:
                file.write("%s - %s\n" % (item[1], item[0]))
        print("Historial exportado a registros.txt")
        time.sleep(5)

export_thread = threading.Thread(target=export_history)
export_thread.start()

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
            result = face_recognition.compare_faces([face_frame_encodings], reference_face_encoding)

            if result[0]:
                text = "Jorman"
                color = (125, 228, 0)
            else:
                text = "Desconocido"
                color = (50, 50, 255)

            cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
            cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
            cv2.putText(frame, text, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)


            recognized_history.append((text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()
