import cv2
import numpy as np
import datetime

cap = cv2.VideoCapture("VIDEO.avi")
#cap = cv2.VideoCapture("test.avi")
StructureCounter = 0
BreadCounter = 0
none, frame1 = cap.read()
none, frame2 = cap.read()
##
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ', ', y)
##
point1 = (557 ,  108)
point2 = (557 ,  340)


while cap.isOpened():
    frame1 = cv2.line(frame1, point1, point2, (0, 0, 255), 2)
    frame2 = cv2.line(frame2, point1, point2, (0, 0, 255), 2)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    none, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations = 3)
    contours, none = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        ##### DE MODIFICAT VALOAREA - (POSIBIL ADAPTIVA) 900 - test 5000 - test2 #####
        if cv2.contourArea(contour) < 15000:
            continue

        frame1 = cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        CentruObiectDetectat = (int((x+x+w)/2), int((y+y+h)/2))
        cv2.circle(frame1, CentruObiectDetectat, 1, (0, 0, 0), 5)

        if abs(CentruObiectDetectat[0] - point1[0]) < 60 and not StructureCounter:
            print(CentruObiectDetectat[0], ', ', point1[0])
            StructureCounter = 1
            BreadCounter = BreadCounter + 1
            print(datetime.datetime.now())
        else:
            StructureCounter = 0

    cv2.putText(frame1, "Counter: {}".format(BreadCounter), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 255, 0), 2, 2)

    cv2.imshow("Frame", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    ##
    cv2.setMouseCallback('Frame', click_event)
    ##
    if not ret:
        print("A aparut o eroare!")

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()