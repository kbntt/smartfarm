import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret, img_color = cap.read()

    if not ret:
        break

    img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)

    cv.imshow('bgr', img_color)
    cv.imshow('gray', img_gray)

    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()
