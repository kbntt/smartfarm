import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret, img_color = cap.read()

    if not ret:
        break

    cv.imshow('bgr', img_color)

    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()
