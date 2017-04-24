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


def genHueDiff(image, mask):
    """This function finds differences between the image and the mask

    Parameters
    ----------
    image : numpy.ndarray
        An image
    mask : numpy.ndarray
        A mask

    Returns
    -------
    [(int, int), ...]
        The image with the hue changed
    """

    hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsvMsk = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
    hueDiff = []

    for i in xrange(len(hsvImg)):
        for j in xrange(len(hsvImg[0])):
            if (hsvImg[i][j] != hsvMsk[i][j]).any():
                hueDiff.append(((hsvImg[i][j][0], hsvImg[i][j][1], hsvImg[i][j][2]), (hsvMsk[i][j][0], hsvMsk[i][j][1], hsvMsk[i][j][2]), (i,j)))

    return list(set(hueDiff))

def changeHVPos(hsvImg, imgMark, tp, pos, hwidth, swidth, vwidth, stack):
    """Chanes the hue and value starting at at the given position

    Parameters
    ----------
    hsvImg : numpy.ndarray
        An image
    imgMark : numpy.ndarry (np.bool)
        marks the spaces overwritten
    trans : translation tuple
    pos : The position

    """

    # check to see if the spot has been checked or is out of bounds
    if pos[0] < 0 or pos[0] >= len(hsvImg) or pos[1] < 0 or pos[1] >= len(hsvImg[0]) or imgMark[pos[0]][pos[1]]:
        return

    pix = hsvImg[pos[0]][pos[1]]

    hdst = abs(int(tp[0][0])-pix[0])
    if hdst >= 180:
        hdst = 180 - hdst
    sdst = abs(int(tp[0][1])-pix[1])
    if sdst >= 256:
        sdst = 256 - sdst
    vdst = abs(int(tp[0][2])-pix[2])
    if vdst >= 256:
        vdst = 256 - vdst

    if hdst < hwidth/2 and sdst < swidth/2 and vdst < vwidth/2:
        nh = int(tp[1][0])-tp[0][0] + pix[0]
        if nh < 0:
            nh += 180
        elif nh >= 180:
            nh -= 180
        pix[0] = nh

        #nv = int(tp[1][2])-tp[0][2] + pix[2]
        #if nv < 0:
        #    nv = 0
        #elif nv >= 256:
        #    nv = 255
        #pix[2] = nv

        imgMark[pos[0]][pos[1]] = True
        stack.append((pos[0]+1, pos[1]))
        stack.append((pos[0]-1, pos[1]))
        stack.append((pos[0], pos[1]+1))
        stack.append((pos[0], pos[1]-1))


def changeHV(image, tPairs, hwidth=18, swidth=128, vwidth=128):
    """This function changes the hue and value in the image starting at the given point

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
    im = np.full((len(image), len(image[0])), False, dtype=bool)

    for tp in tPairs:
        st = []
        st.append(tp[2])
        while 0 != len(st):
            changeHVPos(hsv, im, tp, st.pop(), hwidth, swidth, vwidth, st)

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def changeHue(image, tPairs, hwidth=18, vwidth=512):
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
            for tp in tPairs:
                hdst = abs(int(tp[0][0])-pix[0])
                if hdst >= 180:
                    hdst = 180 - hdst
                vdst = abs(int(tp[0][2])-pix[2])
                if vdst >= 256:
                    vdst = 256 - vdst
                if hdst < hwidth/2 and vdst < vwidth/2:
                    nh = int(tp[1][0])-tp[0][0] + pix[0]
                    if nh < 0:
                        nh += 180
                    elif nh >= 180:
                        nh -= 180

                    pix[0] = nh

                    #nv = int(tp[1][1])-tp[0][1] + pix[2]
                    #if nv < 0:
                    #    nv = 0
                    #elif nv >= 256:
                    #    nv = 255

                    #pix[2] = nv
                    break

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def histCenters(hueHst, width=18):
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

