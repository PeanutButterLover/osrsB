# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy
import time
import pyautogui
 
def waitForRock(rockLib):
    """Checks to see if the proper message is on screen to indicate that the rock is ready to mine"""
    imgRockGood = rockLib[0], rockLib[1], rockLib[2]
    imgMined = rockLib[4]
    while imageMatch(imgRockGood, imgMined) == False:
        time.sleep((0.1, 1))
    return imageMatch(imgRockGood, imgMined)
 
def imageMatch(imgMined, imgRockGood):
    pyautogui.screenshot('images/screenshot.png', region=imgRockGood)
    screen = cv2.imread('images/screenshot.png')
    template = cv2.imread(imgMined)
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = .80
    loc = numpy.where(res >= threshold)
    if len(loc[0]) > 0:
        return True
    return False
 
rockLib = {'rock1': (630, 367, 350, 200, 'images/ironMined.png'),
           'rock1Mined': (630, 367, 275, 200, 'images/ironUnmined.png'),
            'rock2': (1144, 695, 350, 200, 'images/ironMined.png'),
            'rock2Mined': (1144, 695, 275, 200, 'images/ironUnmined.png'),
            'rock3': (1128, 691, 350, 200, 'images/ironMined.png'),
            'rock3Mined': (1128, 691, 275, 200, 'images/ironUnmined.png')}

imageMatch(rockLib[0], rockLib[1])