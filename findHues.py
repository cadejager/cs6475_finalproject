import errno
import os
import sys

import numpy as np
import cv2

from glob import glob

import finalproject as fp

# this function will find the dominate hues in an image
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Usage: %s FILE" % (sys.argv[0])
        sys.exit(1)

    print "Reading image"
    image = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

    print "Getting hue hist"
    hist = fp.hueHist(image)

    print "Finding Hist Centers"
    print fp.histCenters(hist)


