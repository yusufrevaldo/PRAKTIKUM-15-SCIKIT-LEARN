import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load model
model = pickle.load(open(r'C:\SEMESTER 6\KONTROL CERDAS\model.pickle', 'rb'))

# Kamera
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

label_dict = {0: 'buka', 1: 'tutup'}

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            for lm in hand_landmarks.landmark:
                x_.append(lm.x)
                y_.append(lm.y)

            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min(x_))
                data_aux.append(lm.y - min(y_))

            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = label_dict[int(prediction[0])]

            cv2.putText(frame, predicted_character,
                        (200, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.3, (0, 255, 0), 3)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()