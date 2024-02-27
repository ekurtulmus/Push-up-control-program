import cv2  # OpenCV kütüphanesini ekliyoruz.
import numpy as np  # Matematiksel işlemler için Numpy kütüphanesini ekliyoruz.
import mediapipe as mp  # Mediapipe kütüphanesini ekliyoruz.
import math  # Matematiksel işlemler için Math kütüphanesini ekliyoruz.

# Belirli bir nokta çifti arasındaki açıyı bulan ve eğer gerekliyse görüntüye çizen bir fonksiyon tanımlıyoruz.
def findAngle(img, p1, p2, p3, lmList, draw=True):
    x1, y1 = lmList[p1][1:]  # p1'in koordinatlarını alıyoruz. (x ve y şeklinde)
    x2, y2 = lmList[p2][1:]  # p2'nin koordinatlarını alıyoruz.
    x3, y3 = lmList[p3][1:]  # p3'ün koordinatlarını alıyoruz.

    # Açıyı hesaplamak için atan2 fonksiyonunu kullanıyoruz.
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:  # Açı negatifse, 360 derece ekleyerek düzeltiyoruz.
        angle += 360

    if draw:  # Eğer draw True ise, çizimler yapılır.
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)  # p1-p2 arasında çizgi çizilir. renk ve kalınlık belirttik
        cv2.line(img, (x3, y3), (x2, y2), (0, 0, 255), 3)  # p2-p3 arasında çizgi çizilir.

        # Noktaların etrafına daireler çizilir.
        cv2.circle(img, (x1, y1), 10, (0, 255, 255), cv2.FILLED)
        cv2. circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (0, 255, 255), cv2.FILLED)

        # Dairelerin etrafına daha büyük daireler çizilir.
        cv2.circle(img, (x1, y1), 15, (0, 255, 255))
        cv2.circle(img, (x2, y2), 15, (0, 255, 255))
        cv2.circle(img, (x3, y3), 15, (0, 255, 255)) #kalınlık ve rengi ayarladık

        # Açının değeri yazılır.
        cv2.putText(img, str(int(angle)), (x2 - 40, y2 + 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
    return angle  # Hesaplanan açı döndürülür. return fonksiyon dışında da döndürebilmemizi sağlar.


# Video akışını alır ve üzerinde belirli bir egzersiz yapılırken açıyı hesaplar.
cap = cv2.VideoCapture("sinav.mp4")  # Video dosyasını okur.

# Mediapipe kütüphanesini kullanarak vücut pozisyonunu belirlemek için gerekli nesneleri oluşturuyoruz.
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

dir = 0  # Yönü kontrol etmek için bir değişken tanımlıyoruz.
count = 0  # Şınav sayısını saklamak için bir değişken tanımlıyoruz.

# Ana döngü
while True:
    success, img = cap.read()  # Bir sonraki kareyi okur.
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Görüntüyü RGB formatına dönüştürür.

    results = pose.process(imgRGB)  # Görüntüyü işler ve vücut pozisyonunu bulur.

    lmList = []  # Vücut parçalarının koordinatlarını saklamak için bir liste oluşturuyoruz.
    if results.pose_landmarks:  # Eğer vücut parçaları tespit edilmişse:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)  # Vücut parçalarını çizer.

        for id, lm in enumerate(results.pose_landmarks.landmark):  # Her bir vücut parçası için:
            h, w, _ = img.shape  # Görüntünün boyutlarını alır.
            cx, cy = int(lm.x * w), int(lm.y * h)  # Oranları kullanarak koordinatları hesaplar.
            lmList.append([id, cx, cy])  # Koordinatları listeye ekler.

    if len(lmList) != 0:  # Eğer vücut parçaları tespit edilmişse:
        angle = findAngle(img, 12, 14, 16, lmList)  # Belirli bir açıyı hesaplar. 12,14,16 vücuttaki sağ kol kısmını temsil eder.
        per = np.interp(angle, (65, 145), (0, 100))  # Açıyı yüzde cinsine çevirir. Hareket 65 ile 145 arasındaysa kabul eder

        # Yapılan şınav sayısını günceller.
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0

        print(count)  # Şınav sayısını ekrana yazdırır.

        # Sayıyı ekrana yazdırır.
        cv2.putText(img, str(int(count)), (45, 125), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 10)

    cv2.imshow("image", img)  # Görüntüyü ekranda gösterir.
    cv2.waitKey(1)  # Belirli bir tuşa basıncaya kadar bekler.