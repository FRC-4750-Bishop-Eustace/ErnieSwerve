import cv2
import numpy as np

cap=cv2.VideoCapture(0)
while True:
   #_ is a throwaway variable
   _,frame=cap.read()
   cv2.imshow("Camera Stream".frame)
   cv2.waitKey(1)

frame=cv2.imread("output.jpg")
cropped_img=frame[0:int(frame.shape[0]/2)]
lower_orange=np.array([255,75,0])
upper_orange=np.array([255,165,0])

frame_hsv = cv2.cvtColor(frame,cv2.COLOR_RGB2H5V)
frame_inrange = cv2.inrange(frame_hsv,lower_orange,upper_orange)
cv2.imshow("Camera Stream", frame_inrange)


cv2.findCountours(frame_inrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
   img=cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)
cv2.imshow("CameraStream",img)
cv2.waitKey(0)
