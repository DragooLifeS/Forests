import cv2
import math

#Vcap = "ссылка видео с коптера.mp4"

cap = cv2.VideoCapture('forests.mp4')
frame_count = 0
while True:
    tr, frame = cap.read()
    frame_ = frame.copy()
    if not tr:
        cap = cv2.VideoCapture('forests.mp4')
        tr, frame = cap.read()

    frame_hsv = cv2.cvtColor(frame, 40) # из bgr в hsv(удобнее т.к. на одной оси все цвета)
    # для лиственных
    low = (0, 100, 120)
    high = (65, 255, 255)

    # для хвойных (они темнее)
    low_h = (30, 40, 0)
    high_h = (90, 255, 255)

    # нахождение площади(Илон Маска)
    mask = cv2.inRange(frame_hsv, low, high)
    mask_h = cv2.inRange(frame_hsv, low_h, high_h)
    
    # нахождение контуров
    conts, h = cv2.findContours(mask, cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)
    conts_h, h = cv2.findContours(mask_h, cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)
    # сортировка контуров для удаления самых маленьких т.е. не нужных
    conts = sorted(conts, key=cv2.contourArea,
                   reverse=True)
    conts_h = sorted(conts_h, key=cv2.contourArea,
                   reverse=True)
    # отрисовка контура
    for cont in conts:
        if cv2.contourArea(cont) > 200:
            cv2.drawContours(frame, [cont], -1, (100,200,255), 2)
    for cont in conts_h:
        if cv2.contourArea(cont) > 200:
            cv2.drawContours(frame, [cont], -1, (255,50,100), 2)
    # отрисовка масштаба
    cv2.line(frame, (40,660), (140, 660), (255,255,255), 10)
    cv2.line(frame, (60,660), (80, 660), (0,0,0), 10)
    cv2.line(frame, (100,660), (120, 660), (0,0,0), 10 )
    
    cv2.imshow('forest', frame)
    #cv2.imshow('list', mask)
    #cv2.imshow('hvoya', mask_h)
    key = cv2.waitKey(1) # пауза до нажатия клавиши или пофиг...
                         
    if key == 27:
        break
    if key == 13:
        #cv2.imwrite('frame' + str(frame_count) + '.jpg', frame_)
        cv2.imwrite('marked_frame' + str(frame_count) + '.jpg', frame)
        s = ("%.f" % cv2.contourArea(conts[0]))*0.0265
        s_h = ("%.f" % cv2.contourArea(conts_h[0]))*0.0265

        for i in range(0,50):
            #зависимость реал -> картинка 0,43%!!!!!!!!!

        frame_count += 1
 
cv2.destroyAllWindows() 
