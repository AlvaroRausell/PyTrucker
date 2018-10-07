from random import randint

class Line:
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.avgX = (x1 + x2)/2
        self.avgY = (y1+y2)/2
        self.slope = (y2-y1)/(x2-x1)


class Lane:
    def __init__(self):
        self.lines = []

    def getRandomLine(self):
        if len(self.lines) == 0:
            return  0
        return self.lines[randint(0,len(self.lines)-1)]
    def getAvgX(self):
        try:
            avgX = 0
            for line in self.lines:
                avgX += line.avgX
            return avgX/len(self.lines)
        except:
            return 0


    def getAvgY(self):
        try:
            avgY = 0
            for line in self.lines:
                avgY += line.avgY
            return avgY/len(self.lines)
        except:
            return 0

    def getAvgSlope(self):
        try:
            avgSlope = 0
            for line in self.lines:
                avgSlope += line.slope
            return avgSlope/len(self.lines)
        except:
            return 0
    def add(self,line):

        self.lines.append(line)

class Road:
    def __init__(self,lines):
        self.leftLane = Lane()
        self.rightLane = Lane()
        try:
            if len(lines)> 1:
                self.distributeLines(lines)
        except:
            pass
    def distributeLines(self,lines):
        print("Distributing "+ str(len(lines))+" lines")

        for line in lines:
            line = line[0]
            line = Line(line[0],line[1],line[2],line[3])
            if line.avgX < 450:
                if abs(line.slope)>0.7:
                    self.leftLane.add(line)
            elif  line.avgX > 550:
                if abs(line.slope)>0.7:
                    self.rightLane.add(line)
    def getAvgs(self):
        avgX = (self.leftLane.getAvgX()+self.rightLane.getAvgX())/2
        avgY = (self.leftLane.getAvgY()+self.rightLane.getAvgY())/2
        avgSlope = (self.leftLane.getAvgSlope()+self.rightLane.getAvgSlope())/2

        return avgX,avgY,avgSlope
