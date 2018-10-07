import numpy as np
from PIL import ImageGrab
import cv2
from directXKeys import PressKey,ReleaseKey, W, A, S, D
from laneProcessing import Line, Lane, Road

CENTER = 575
working = True
def draw_lines(img,lines):
        road = Road(lines)
        for line in road.leftLane.lines:
            #print(str(len(road.leftLane.lines)))
            cv2.line(img,(line.x1,line.y1),(line.x2,line.y2),[255,255,255],5)
        for line in road.rightLane.lines:
            cv2.line(img,(line.x1,line.y1),(line.x2,line.y2),[255,255,255],5)
        return road


def move(road,SlopeThreshold,PosThreshold):
    PressKey(W)
    keyIndex = decideMove(road,SlopeThreshold,PosThreshold)
    if keyIndex < 0:
        ReleaseKey(D)
        PressKey(A)

        #while avgX + threshold < CENTER: #MAKE INTO ANOTHER FUNCTION THINGY
        #    print("Moving left")
    elif keyIndex > 0:
        ReleaseKey(A)
        PressKey(D)

        #while avgX - threshold > CENTER: #MAKE INTO ANOTHER FUNCTION THINGY
        #    print("Moving right")
    else:
        ReleaseKey(D)
        ReleaseKey(A)
    ReleaseKey(W)

def decideMove(road, SlopeThreshold,PosThreshold):
        print("Deciding move")
        leftSlope = -road.leftLane.getAvgSlope()
        rightSlope = -road.rightLane.getAvgSlope()
        print("Deciding move32y467")
        # print(avgSlope)
        # if avgSlope<0-SlopeThreshold:
        #     return -1
        # elif avgSlope>0+SlopeThreshold:
        #     return 1
        #else:
        print("L: "+str(leftSlope)+" R:"+str(rightSlope))
        if leftSlope + SlopeThreshold <0 and rightSlope +SlopeThreshold < 0:# or avgX <525:
            print( "Left")
            return -1
        elif leftSlope - SlopeThreshold>0 and rightSlope  - SlopeThreshold> 0:#  or avgX > 540:
            print("Right")
            return 1
        print("Center")
        return 0


def regionOfInterest(img,vertices):
    region = np.zeros_like(img)
    cv2.fillPoly(region,vertices,255)
    region = cv2.bitwise_and(img,region)
    return region

def getEdges(img):
    processedImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    processedImg = cv2.Canny(processedImg,100,250)
    vertices = np.array([[400,425],[400,355],[750,355],[750,425]])
    #processedImg = regionOfInterest(processedImg,[vertices])
    processedImg = cv2.GaussianBlur(processedImg,(7,7),0)
    lines = cv2.HoughLinesP(processedImg,1,np.pi/180,15,np.array([]),10,100)
    road = draw_lines(processedImg,lines)
    return road, processedImg

while True:
    screen = ImageGrab.grab(bbox=(0,40,700,750))
    lines,edges = getEdges(np.array(screen))
    cv2.imshow("Image",edges)
    try:
        if working:
           move(lines,0.5,75)
    except:
        pass
    if cv2.waitKey(25) & 0xFF == ord('q'):
        working = not working
