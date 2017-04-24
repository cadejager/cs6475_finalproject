import errno
import os
import sys

import numpy as np
import cv2

from glob import glob

import finalproject as fp

# this function will find the dominate hues in an image
if __name__ == "__main__":

    if len(sys.argv) != 4:
        print "Usage: %s INPUT MASK OUTPUT" % (sys.argv[0])
        sys.exit(1)

    print "Reading images"
    image = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    mask = cv2.imread(sys.argv[2], cv2.IMREAD_COLOR)

    print "finding hue changes"
    hd = fp.genHueDiff(image, mask)
    print "hue changes " + str(hd)

    print "changing Hues"
    #image = fp.changeHV(image, hd)

    #hu = [((9, 0, 0), (9+90, 0, 0)), ((102, 0, 0), (60, 0, 0))]
    image = fp.changeHue(image, hd)

    print "writing image"
    cv2.imwrite(sys.argv[3], image)


