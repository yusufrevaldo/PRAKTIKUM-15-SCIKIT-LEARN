import os
import cv2

DATA_DIR = r'C:\SEMESTER 6\KONTROL CERDAS\DATA'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 2
dataset_size = 100

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Kamera tidak terdeteksi!")
    exit()

for j in range(number_of_classes):

    class_path = os.path.join(DATA_DIR, str(j))
    os.makedirs(class_path, exist_ok=True)

    print('Collecting data for class {}'.format(j))
    print('Tekan Q untuk mulai capture')

    # Tunggu tekan Q
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal baca kamera")
            break

        cv2.putText(frame, 'Ready? Press Q!',
                    (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Mulai ambil gambar
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Gagal baca kamera")
            break

        cv2.imshow('frame', frame)
        cv2.imwrite(os.path.join(class_path, f'{counter}.jpg'), frame)
        cv2.waitKey(50)
        counter += 1

print("Selesai ambil data!")

cap.release()
cv2.destroyAllWindows()