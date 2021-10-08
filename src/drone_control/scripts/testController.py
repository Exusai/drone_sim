#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import CompressedImage, Image
import numpy as np
import cv2 as cv
import sys
from scipy import signal
from scipy import misc

#/ardrone/bottom/image_raw/compressed


def callback(data):
    
    imageRaw = np.fromstring(data.data, np.uint8).reshape(data.height, data.width, -1)
    print("Tamaño de la img recivida: ", np.shape(imageRaw))

    normImg = imageRaw/255
    scharr = np.array([[ -3-3j, 0-10j,  +3 -3j],
                    [-10+0j, 0+ 0j, +10 +0j],
                    [ -3+3j, 0+10j,  +3 +3j]]) # Gx + j*Gy
    grad = signal.convolve2d(normImg[:,:,1], scharr, boundary='symm', mode='same')

    #image = imageRaw/255
    convImg = np.absolute(grad)
    #print(image)
    cv.imshow("Convolucin",convImg)
    cv.imshow("Prueba Video",normImg)
    cv.waitKey(1)
        


### F. N_callback
def listener():
    rospy.init_node('image_viewer', anonymous=True)
    rospy.Subscriber('/ardrone/front/image_raw/', Image, callback)
    rospy.spin()

### main
if __name__ == '__main__':
    print('Iniciando')
    try:
        listener()
    except:
        cv.destroyAllWindows()
        sys.exit()

