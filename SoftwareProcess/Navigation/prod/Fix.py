from datetime import datetime
from xml.dom import minidom
import math
from cmath import sqrt
import Angle
from math import tan

class Fix():
    def __init__(self, logFile = "log.txt"):
        if(isinstance(logFile, basestring)):
            checkForPeriod = logFile.find(".")
            if(checkForPeriod != -1):
                enteredFileType = logFile[checkForPeriod + 1: len(logFile)]
                if(enteredFileType != "txt"):
                    raise ValueError("Fix.__init__: The file violates the parameter rules")                    
                
            self.log = logFile
            f = open(self.log, "w+")
            f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Start of log\n")
        else:
            raise ValueError("Fix.__init__: The file violates the parameter rules")
        
    def setSightingFile(self, sightingFile):    
        if(isinstance(sightingFile, basestring)):
            checkForPeriod = sightingFile.find(".")
            if(checkForPeriod != -1):
                enteredFileType = sightingFile[checkForPeriod + 1: len(sightingFile)]
                if(enteredFileType != "xml"):
                    raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
                
            f = open(self.log, "a")
            f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Start of sighting file: " + sightingFile + "\n")
            
            s = open(sightingFile, "r")
            self.strOfSightingFile = s.read()
            s.close()
            return self.strOfSightingFile
        else:
            raise ValueError("Fix.setSightingFile: The file violates the parameter rules")
    
    def getBody(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        bodyList = xmlDocument.getElementsByTagName('body')
        self.body = bodyList[count].firstChild.nodeValue
        return self.body
    
    def getDate(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        dateList = xmlDocument.getElementsByTagName('date')
        self.date = dateList[count].firstChild.nodeValue
        return self.date
    
    def getTime(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        timeList = xmlDocument.getElementsByTagName('time')
        self.time = timeList[count].firstChild.nodeValue
        return self.time
    
    def getObservation(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        observationList = xmlDocument.getElementsByTagName('observation')
        self.observation = observationList[count].firstChild.nodeValue
        return self.observation
        
    def getHeight(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        heightList = xmlDocument.getElementsByTagName('height')
        self.height = heightList[count].firstChild.nodeValue
        return self.height
        
    def getTemp(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        tempList = xmlDocument.getElementsByTagName('temperature')
        self.temp = tempList[count].firstChild.nodeValue
        return self.temp
        
    def getPressure(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        pressureList = xmlDocument.getElementsByTagName('pressure')
        self.pressure = pressureList[count].firstChild.nodeValue
        return self.pressure
        
    def getHorizon(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        horizonList = xmlDocument.getElementsByTagName('horizon')
        self.horizon = horizonList[count].firstChild.nodeValue
        return self.horizon
        
    def setSighting(self):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        sightingList = xmlDocument.getElementsByTagName('sighting')
        amount = len(sightingList)
        usedAngle = Angle.Angle()
        for i in range(0, amount):
            self.getBody(i)
            self.getDate(i)
            self.getHeight(i)
            self.getHorizon(i)
            self.getObservation(i)
            self.getPressure(i)
            self.getTemp(i)
            self.getTime(i)
            convertedObs = usedAngle.setDegreesAndMinutes(self.observation)
            altitude = usedAngle.getDegrees()
            #if(self.horizon == "Natural"):
            #    self.dip = (-0.97 * sqrt(int(self.height))) / 60
            #else:
            #    self.dip = 0
            #self.refraction = (-0.00452 * int(self.pressure)) / (273 + ((5/9) * (int(self.temp) - 32))) / tan(altitude)
            #self.adjustedAltitude = (tan(altitude)) + self.dip + self.refraction
            f = open(self.log, "a")
            f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + self.body + "\t" + self.date + "\t" + self.time + "\t" + self.observation + "\n")

        appLatitude = "0d0.0"
        appLongitude = "0d0.0"
        return (appLatitude, appLongitude)
        #f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "End of sighting file: " + sightingFile + "\n") 