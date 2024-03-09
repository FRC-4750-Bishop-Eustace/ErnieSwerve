import cv2
import numpy as np

frame_hsv = cv2.cvtColor(frame,cv2.COLOR_RGB2H5V)
frame_inrange = cv2.inrange(frame_hsv,lower_orange,upper_orange)
cv2.imshow("Camera Stream", frame_inrange)


cv2.findCountours(frame_inrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
   img=cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)
cv2.imshow("CameraStream",img)
cv2.waitKey(0)
