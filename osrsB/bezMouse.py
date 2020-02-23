import pyautogui
import random
import scipy
import time
from scipy import interpolate

def createBezCurve(xLocStart, yLocStart, xLocEnd, yLocEnd): #Coords are flipped for why
    cp = random.randint(2, 4)  # Number of control points. Must be at least 2.
    xLocStart = (xLocStart + random.randint(0, 3))
    yLocStart = (yLocStart + random.randint(0, 3))
    xLocEnd = (xLocEnd + random.randint(0, 3))
    yLocEnd = (yLocEnd + random.randint(0, 3))
    x1, y1 = xLocStart, yLocStart  # Starting position
    x2, y2 = xLocEnd, yLocEnd # Destination
    
    # Distribute control points between start and destination evenly.
    x = scipy.linspace(x1, x2, num=cp, dtype='int')
    y = scipy.linspace(y1, y2, num=cp, dtype='int')
    
    # Randomise inner points a bit (+-RND at most).
    RND = 10
    xr = scipy.random.randint(-RND, RND, size=cp)
    yr = scipy.random.randint(-RND, RND, size=cp)
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr
    
    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
                                      # Must be less than number of control points.
    tck, u = scipy.interpolate.splprep([x, y], k=degree)
    u = scipy.linspace(0, 1, num=max(pyautogui.size()))
    points = scipy.interpolate.splev(u, tck)
    
    # Move mouse.
    pyautogui.PAUSE = 0
    for point in zip(*(i.astype(int) for i in points)):
        pyautogui.moveTo(*point)
    time.sleep((random.randint(2, 4))/10)
    
def createBezCurveMine(xLocStart, yLocStart, xLocEnd, yLocEnd): #Coords are flipped for why
    cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
    xLocEnd = (xLocEnd + random.randint(20, 40))
    yLocEnd = (yLocEnd + random.randint(20, 40))
    x1, y1 = xLocStart, yLocStart  # Starting position
    x2, y2 = xLocEnd, yLocEnd # Destination
    
    # Distribute control points between start and destination evenly.
    x = scipy.linspace(x1, x2, num=cp, dtype='int')
    y = scipy.linspace(y1, y2, num=cp, dtype='int')
    
    # Randomise inner points a bit (+-RND at most).
    RND = 10
    xr = scipy.random.randint(-RND, RND, size=cp)
    yr = scipy.random.randint(-RND, RND, size=cp)
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr
    
    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
                                      # Must be less than number of control points.
    tck, u = scipy.interpolate.splprep([x, y], k=degree)
    u = scipy.linspace(0, 1, num=max(pyautogui.size()))
    points = scipy.interpolate.splev(u, tck)
    
    # Move mouse.
    pyautogui.PAUSE = 0
    for point in zip(*(i.astype(int) for i in points)):
        pyautogui.moveTo(*point)
    time.sleep((random.randint(2, 4))/10)