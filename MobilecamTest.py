import cv2

url = "http://100.115.192.101:8080/video"



while True:
    cap = cv2.VideoCapture(url)
    print("on...")
    ret,frame = cap.read()
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0XFF==ord('q'):
        break