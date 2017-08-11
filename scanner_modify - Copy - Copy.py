import sys
import timepass
# import the necessary packages
import imutils
import cv2
import os
import socket
 
sys.path.append('/usr/local/lib/python2.7/site-packages')

from sys import argv
import zbar
from PIL import Image
import glob
import cv2
import numpy as np
import math
counter_x=0
counter_y=1
read_qr=0
# create a reader
scanner = zbar.ImageScanner()
input_img ='final40.jpg'
# configure the reader
scanner.parse_config('enable')
inst=timepass.App()
# obtain image data
for filename in glob.glob(input_img):
    print filename
    pil = Image.open(filename).convert('L')
    width, height = pil.size
    #raw = pil.tobytes()
    raw=pil.tostring()

    # wrap image data

    
    image = zbar.Image(width, height, 'Y800', raw)
    
    alphabet=inst.clicked1()
    alphabet=alphabet.lower()
    M=list(alphabet)
    
    # scan the image for barcodes
    scanner.scan(image)
    L=[]
    D={}
    X=[]
    D1={}
    abc=[]
    # extract results
    for symbol in image:
        # do something useful with results
        
        L.append(symbol.data)
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        print symbol.location

        topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = [item for item in symbol.location]

        x1=(topLeftCorners[0]+bottomLeftCorners[0])/2
        y1=(topLeftCorners[1]+bottomLeftCorners[1])/2

        x2=(topRightCorners[0]+bottomRightCorners[0])/2
        y2=(topRightCorners[1]+bottomRightCorners[1])/2


        x3=(topLeftCorners[0]+topRightCorners[0])/2
        y3=(topRightCorners[1]+bottomRightCorners[1])/2


        x4=(bottomLeftCorners[0]+bottomRightCorners[0])/2
        y4=(bottomLeftCorners[1]+bottomRightCorners[1])/2

        mid1=(x1+x2)/2
        mid2=(y1+y2)/2

        if symbol.data in D:
             D[symbol.data].append(mid1)
             D[symbol.data].append(mid2)
        else:
            D[symbol.data]=([mid1,mid2])
        read_qr+=1
    img=cv2.imread(input_img,cv2.IMREAD_COLOR)
    font = cv2.FONT_HERSHEY_SIMPLEX
    print 'No of decoded symbols :',read_qr
    print D

    #Image Text on Screen
    for i in L:
        if i in M:
            counter_x=0
            counter_y=1
            if i in X:
                counter_x+=2
                counter_y+=2
                cv2.putText(img,i,(D[i][counter_x],D[i][counter_y]), font, 4,(255,0,0),2)
                D1[i].append(D[i][counter_x])
                D1[i].append(D[i][counter_y])
            else:
                cv2.putText(img,i,(D[i][0],D[i][1]), font, 4,(255,0,0),2)
                D1[i]=[D[i][0],D[i][1]]
                
            X.append(i)

print('The alphabets present on the board are: ')
print(L)    #All Alphabets on screen
print('The alphabets on the board matching with the GUI are: ')
print(X)    #Common alphabets 
print('The matching alphabets and their coordinates are: ')
print(D1)   #Dictionary with co-ordinates

Dnew={}  #NEW CORDINATES WRT BOARD
Dpol={}  #NEW POLAR CORDINATES WRT BOARD



############################################################



# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(input_img)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
#cv2.imshow("GBlurr",gray)
 
# threshold the image, then perform a series of erosions +
# dilations to remove any small regions of noise
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY_INV)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)
#cv2.imshow("Threshold",thresh)

 
# find contours in thresholded image, then grab the largest
# one
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
c = max(cnts, key=cv2.contourArea)

M = cv2.moments(c)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
cX=2343
cY=2230
print 'Board Centre X:',cX
print 'Board Centre Y:',cY

# determine the most extreme points along the contour
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

# draw the outline of the object, then draw each of the
# extreme points, where the left-most is red, right-most
# is green, top-most is blue, and bottom-most is teal
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)
 
# show the output image
#cv2.imshow("Image", image)
#cv2.waitKey(0)


###########################################################

for key,value in D1.items():
    for i in range(0,len(value),2):

        #BOARD CENTER CORDINATES : 350 250  , 1200 2000
        x=int(value[i])-cX   
        y=int(value[i+1])-cY
        y=-y
        
        mod=math.sqrt((x**2)+(y**2))
        ang=math.degrees(math.atan2(y,x))
        if ang<0:
            ang=360+ang
        if key in Dnew:
            Dnew[key].append(x)
            Dnew[key].append(y)
        else:
            Dnew[key]=[x,y]
        if key in Dpol:
            Dpol[key].append(ang)
        else:
            Dpol[key]=[ang]
            
#Printing DNEW
final_r1={}
for key,value in Dnew.items():
    for i in range(0,len(value),2):
        print 'New co-ordinate of ',key, ': ',value[i],',',value[i+1]
        r1=math.sqrt((((abs(value[i])-cX))*2.54/96)**2+(((abs(value[i+1])-cY))*2.54/96)**2)
        if key in final_r1:
            final_r1[key].append(r1)
        else:
            final_r1[key]=[r1]
print final_r1
final_temp={}#Dcit for storing temp angle
#Printing DPOL
for key,value in Dpol.items():
    for i in range(0,len(value),1):
        print 'Angle of ',key,':',value[i]
        value[i]=int(value[i])-12
        if key in final_temp:
            final_temp[key].append(value[i])
        else:
            final_temp[key]=[value[i]]
       
print final_temp
cv2.namedWindow('QR_positions',cv2.WINDOW_NORMAL)
cv2.imshow('QR_positions',img)
cv2.waitKey(0)
######################################
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
for key,value in Dpol.items():
    for i in range(0,len(value),1):
        
        #sock.sendto(str('Angle of %s'% key).encode(),(host,port))
        host='192.168.43.69'
        port=8080
        sock.sendto(str(value[i]).encode(),(host,port))
        #print value[i]
final_angle={}
for key,value in final_temp.items():
    for i in range(0,len(value),1):
        temp=value[i]
        if temp>0 and temp<45:
            alpha=0
        elif temp>45 and temp<90:
            alpha=45
        elif temp>90 and temp<135:
            alpha=90
        elif temp>135 and temp<180:
            alpha=135
        elif temp>180 and temp<225:
            alpha=180
        elif temp>225 and temp<270:
            alpha=225
        elif temp>270 and temp<315:
            alpha=270
        elif temp>315 and temp<360:
            alpha=315
        final=temp-alpha
        #print final
        #r1=50
        r1=final_r1[key][i]
        print r1
        r2=25
        r3=25
        for j in range(1,45,1):
            r4=math.sqrt(math.pow(r1,2)+math.pow(r2,2)-(2*r1*r2*math.cos(math.radians(final))))
            #print 'Value of r4:',r4
            if int(r4)==r3:
                break
            elif r4>r3:
                final-=1    
            elif r4<r3:
                final+=1
            
            #
            #print 'Iteration:',j
        print 'Value of angle:',final
        print 'Final Value of r4:',r4
        id1=temp-final
        if id1<0:
            id1=360-abs(id1)
        print 'Alpha :',id1
        beta=(r2**2+r4**2-r1**2)/(2*r2*r4)
        beta=math.degrees(math.acos(beta))
        print 'Beta:',beta
        #beta=180-beta
        #print beta
        if key in final_angle:
            final_angle[key].append(id1)
            final_angle[key].append(beta)
        else:
            final_angle[key]=[id1,beta]

print final_angle

# clean up
del(image)

