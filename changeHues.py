import errno
import os
import sys

import numpy as np
import cv2

from glob import glob

import finalproject as fp

# this function will find the dominate hues in an image
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Usage: %s INPUT OUTPUT" % (sys.argv[0])
        sys.exit(1)

    print "Reading image"
    image = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

    print "changing Hues"
    image = fp.changeHue(image, 101, 145, width=30)
    image = fp.changeHue(image, 28, 60, width=45)
    #image = fp.changeHue(image, 8, 8+90)

    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)


    print "writing image"
    cv2.imwrite(sys.argv[2], image)


