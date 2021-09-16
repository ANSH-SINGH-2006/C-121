from os import access
import cv2
import time
import numpy as np

#to save the output in the file output.avi
fourcc= cv2.VideoWriter_fourcc(*'XVID')
output_file= cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#starting the webcam
cap=cv2.VideoCapture(0)
time.sleep(2)
bg=0
#capturing the background for 60 seconds
for i in range(60):
    ret, bg= cap.read()
#fliping the background as cam clicks it inverted
bg=np.flip(bg, axis=1)
#reading the captured frame or every frame in bg until the cam is open
while(cap.isOpened()):
    ret,img= cap.read()
    if not ret:
        break
    #flipping the img
    img=np.flip(img, axis=1)
    #converting bgr to hsv
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #reading the mask to detect red color
    lower_red= np.array([0, 120, 50])
    upper_red= np.array([10, 255, 255])
    mask_1= cv2.inRange(hsv, lower_red, upper_red)

    lower_red= np.array([170, 120, 70])
    upper_red= np.array([180, 255, 255])
    mask_2= cv2.inRange(hsv, lower_red, upper_red)

    mask_1=mask_1+mask_2

    mask_1=cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1=cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    #collecting only the part that doesnt have mask 1 and saving in mask 2
    mask_2= cv2.bitwise_not(mask_1)
    #keeping only images which excluded red color part
    res_1= cv2.bitwise_and(img, img, mask=mask_2)
    #keeping only the part of imgs with red color
    res_2= cv2.bitwise_and(bg, bg, mask=mask_1)
    #generating the final output after merging the res1 and res2
    final_output= cv2.addWeighted(res_1, 1, res_2, 1,0)
    output_file.write(final_output)

    #displaying the output to the user
    cv2.imshow('magic', final_output)

    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()