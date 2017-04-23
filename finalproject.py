# ASSIGNMENT 11
# Chris DeJager

""" Final Project
"""

import numpy as np
import scipy as sp
import cv2
import scipy.signal

def fil(width, alpha=0.5):
    """Returns a filter to use

    Parameters
    ----------
    width : int
        The width of the filter
    alpha : float
        A parameter

    Returns
    -------
    numpy.ndarray(dtype: np.float)
        A widthx1 numpy array representing the filter.
    """
    fil = np.zeros(width, dtype=np.float64)

    hd = width/2.

    for i in xrange(width):
        cendst = hd - abs(i-hd)

        fil[i] = ((1-alpha) + 2*alpha*(cendst/hd)) / width

    return fil


def hueHist(image):
    """This function takes a color image and returns a histogram of the hues in
    that image

    Parameters
    ----------
    image : numpy.ndarray
        An image

    Returns
    -------
    numpy.ndarray(dtype=np.uint32)
        a hue hist
    """
    outhst = np.zeros(180, dtype=np.uint32)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    for row in hsv:
        for pix in row:
            outhst[pix[0]] += 1

    return outhst

def changeHue(image, huePairs, width=22):
    """This function changes the hue in the image

    Parameters
    ----------
    image : numpy.ndarray
        An image
    huePairs : (int, int)[]
        The converion to due to the hues
    width : 
        The width of the hue

    Returns
    -------
    numpy.ndarray
        The image with the hue changed
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    for row in hsv:
        for pix in row:
            for hp in huePairs:
                dst = abs(hp[0]-pix[0])
                if dst >= 180:
                    dst = 180 - dst
                if dst < width/2:
                    nh = hp[1]-hp[0] + pix[0]
                    if nh < 0:
                        nh += 180
                    elif nh >= 180:
                        nh -= 180

                    pix[0] = nh
                    break

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def histCenters(hueHst, width=22):
    """This function finds the best color centers at the given hue width

    Parameters
    ----------
    hueHst : numpy.uint32
        A histagram of hues in the image
    width : int
        The width to find the best hues in the image

    Returns
    -------
    list
        A list of the best centers to use
    """
    avgHst = np.zeros(180, dtype=np.float64)
    f = fil(width)

    for i in xrange(180):
        for j in xrange(width):
            pos = i+j-(width/2)
            if pos < 0:
                pos += 180
            elif pos >= 180:
                pos -= 180

            avgHst[i] += f[j]*hueHst[pos]

    ouths = [(0, avgHst[0])]

    for i in xrange(180):
        best = True
        for ht in ouths:
            dst = abs(i-ht[0])
            if dst > 90:
                dst = 180 - dst
            if dst < width/2 and ht[1] >= avgHst[i]:
                best = False

        if best == True:
            for ht in ouths:
                dst = abs(i-ht[0])
                if dst > 90:
                    dst = 180 - dst
                if dst < width/2 and ht[1] < avgHst[i]:
                    ouths.remove(ht)

            ouths.append((i, avgHst[i]))

    ouths = sorted(ouths, key=lambda ht: ht[1], reverse=True)

    return ouths

