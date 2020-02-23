# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:08:15 2020

@author: Brad
"""

import pyautogui
import cv2
import time
import numpy as np
import glob
from bezMouse import createBezCurve, createBezCurveMine
import random

region = []
ironImg = 'C:\\osrsB\\images\\ironRock.png'
screenshotFilePath = 'C:\\osrsB\\images\\screenshot.png'
imgScreenRGB = cv2.imread(screenshotFilePath)
imgTextInvenFull = cv2.imread('C:\\osrsB\\images\\invenFullText.png', 0)

imgList = glob.glob('C:\\osrsB\\images\\iron\\*.png') #Create list for iron rocks
data = []
for k in imgList:
    data.append(k)
grayList = []
for img in data:
    imageConvert = cv2.imread(img)
    grayList.append(cv2.cvtColor(imageConvert, cv2.COLOR_BGR2GRAY))

imgIronInvenList = glob.glob('C:\\osrsB\\images\\fullInvenIron\\*.png') #Create list for inventory
dataInven = []
for j in imgIronInvenList:
    dataInven.append(j)
invenList = []
for imgInven in dataInven:
    imageConvert = cv2.imread(imgInven)
    invenList.append(cv2.cvtColor(imageConvert, cv2.COLOR_BGR2GRAY))

def takeScreenshotAndPass(): #Function call to take screenshot and pass the cv gray image
    pyautogui.screenshot(screenshotFilePath)
    imgScreenRGB = cv2.imread(screenshotFilePath)
    imgScreenGray = cv2.cvtColor(imgScreenRGB, cv2.COLOR_BGR2GRAY)
    return imgScreenGray
    
def checkForRocksToMine(grayList): #Takes gray template items and match to screenshot, returns locations of items
    threshold = 0.8
    imgScreenGray = takeScreenshotAndPass()
    rockNupyList = []
    for template in grayList: 
        res = cv2.matchTemplate(imgScreenGray, template, cv2.TM_CCOEFF_NORMED)
        locRockToMine = np.array((np.where(res >= threshold)))
        if locRockToMine.size != 0:
            rockNupyList.append(locRockToMine)
    return rockNupyList

def clickAndDropInven(locInvenDrop): #Does not click first slot as it will be pick
    time.sleep((random.randint(1, 3)))
    locDrop = locInvenDrop
    pyautogui.keyDown('shift')
    for k in range(len(locDrop[0])-1):
        createBezCurve(locDrop[1][k], locDrop[0][k], locDrop[1][k+1], locDrop[0][k+1])
        pyautogui.click(button='left')
    pyautogui.keyUp('shift')
        
def mineRock(): #Views screenshot and finds rocks to mine
    global nextMineTime
    nextMineTime = time.time()
    nextMineTime = nextMineTime+8
    locsToMine = checkForRocksToMine(grayList)
    #time.sleep(((random.randrange(1, 2)/10)))
    rockMineLen = len(locsToMine)
    if rockMineLen == 0: #Checks for mineable locations, if not found waits and calls again
        #time.sleep(((random.randrange(1, 5)/10)))
        mineRock()
    else:
        threshold = 0.8
        res = cv2.matchTemplate(imgScreenGray, template, cv2.TM_CCOEFF_NORMED)
        invenText = np.where(res >= threshold)
        rockChoose = random.randrange(0, rockMineLen) #Picks rocks from list to mine
        x1, y1 = pyautogui.position()
        createBezCurveMine(x1, y1, random.choice(locsToMine[rockChoose][1]), random.choice(locsToMine[rockChoose][0]))
        pyautogui.click(button='left')
        preMineRockCount = currentRockCount()
        waitForEvent(preMineRockCount)

def currentRockCount():
    threshold = 0.97
    imgScreenGray = takeScreenshotAndPass()
    locInvenList = []
    for template in invenList: 
        res = cv2.matchTemplate(imgScreenGray, template, cv2.TM_CCOEFF_NORMED)
        locInven = np.array((np.where(res >= threshold)))
#        for pt in zip(*locInven[::-1]): #view what is being highlighted
#            w, h = template.shape[::-1]
#            cv2.rectangle(imgScreenRGB, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2) 
#        cv2.imwrite('res.png', imgScreenRGB)
        if locInven.size != 0:
            locInvenList.append(locInven)
    locInvenNumpySingleX = []
    locInvenNumpySingleY = []
    for k in range(len(locInvenList)):
        locInvenNumpySingleX.extend(locInvenList[k][0])
        locInvenNumpySingleY.extend(locInvenList[k][1])
    currentInvenSpaceTaken = (len(locInvenNumpySingleX))
    totalInvenNumpy = np.stack((locInvenNumpySingleX, locInvenNumpySingleY))
    if currentInvenSpaceTaken == 27:
        clickAndDropInven(totalInvenNumpy)
    return currentInvenSpaceTaken

def waitForEvent(preMineRockCount):
    timeMine = time.time()
    preCount = preMineRockCount
    currentRockNum = currentRockCount()
    if currentRockNum > preCount:
        mineRock()
    if  timeMine > nextMineTime:
        mineRock()
    else:
        waitForEvent(preCount)

time.sleep(3)
currentRockCount()
while True:
    mineRock()

''' 
Camera at middle zoom
16	14	16	15	27	19 - Times waitForEvent was called - implement to timeout after 25 or so'''

#def clickLocMine(loc):
#loc = checkForRocksToMine(grayList)
#fullInvenCheck()


#for k in range(len(locDropOres[0])-1):
#    createBezCurve(locDropOres[1][k], locDropOres[0][k], locDropOres[1][k+1], locDropOres[0][k+1])
#for pt in zip(*loc[::-1]): #view what is being highlighted
#            w, h = template.shape[::-1]
#            cv2.rectangle(imgScreenRGB, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2) 
#        cv2.imwrite('res.png', imgScreenRGB)
#    