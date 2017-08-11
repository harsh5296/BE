import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('final40.jpg',0)
edges = cv2.Canny(img,100,200)


ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2) 
#cnt = contours[0]
#M = cv2.moments(cnt)
#print M

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()

centres=[]
print(len(contours))
for i in range(len(contours)):
    moments = cv2.moments(contours[i])
    centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
    cv2.circle(img, centres[-1], 3, (0, 255, 0), -1)

print centres
#cx = int(M['m10']/M['m00'])
#cy = int(M['m01']/M['m00'])
#print cx
#print cy
x,y,w,h = cv2.boundingRect(contours[1])
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#cv2.imshow('image', img)
#cv2.imwrite('test2.png',img)

#plt.show()
#cv2.drawContours(img,[box],0,(0,0,255),2)
#cv2.imshow('test',img1)


