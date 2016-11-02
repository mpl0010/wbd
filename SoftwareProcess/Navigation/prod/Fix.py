from datetime import datetime
from xml.dom import minidom
import math
from cmath import sqrt
import Angle
from math import tan
import os

class Fix():
    def __init__(self, logFile = "log.txt"):
        try:
            self.log = logFile
            self.strOfSightingFile = None
            self.starDictionary = None
            self.ariesDictionary = None
            f = open(self.log, "a")
            f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Log file:\t" + os.path.abspath(self.log) + "\n")
        except:
            raise ValueError("Fix.__init__: The file violates the parameter rules")                    
           
    def setSightingFile(self, sightingFile = None):
        if(isinstance(sightingFile, basestring)):
            if(sightingFile == None):
                raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
            
            checkForPeriod = sightingFile.find(".")
            if(checkForPeriod != -1):
                enteredFileType = sightingFile[checkForPeriod + 1: len(sightingFile)]
                if(enteredFileType != "xml"):
                    raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
            else:
                raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
            
            try:
                self.sightingFile = sightingFile
                f = open(self.log, "a")
                f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Sighting file:\t" + os.path.abspath(self.sightingFile) + "\n")
            
                s = open(sightingFile, "r")
                self.unedittedString = s.read()
                self.strOfSightingFile = self.unedittedString.translate(None, "\t")
                s.close()
                return self.sightingFile
            except:    
                raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
        else:
            raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
             
    def setAriesFile(self, ariesFile):
        if(ariesFile == None):
            raise ValueError("Fix.setAriesFile: The file violates the parameter rules")                    
        
        checkForPeriod = ariesFile.find(".")
        if(checkForPeriod != -1):
            enteredFileType = ariesFile[checkForPeriod + 1: len(ariesFile)]
            if(enteredFileType != "txt"):
                raise ValueError("Fix.setAriesFile: The file violates the parameter rules")                    
        else:
            raise ValueError("Fix.setAriesFile: The file violates the parameter rules")                    
        
        try:
            self.ariesFile = ariesFile
            f = open(self.log, "a")
            f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Aries file:\t" + os.path.abspath(self.ariesFile) + "\n")
        
            ariesDict = {}
            with open(ariesFile) as af:
                for line in af:
                    entry = line.split("\t", 1)
                    date = entry[0]
                    values = entry[1].split()
                    if date in ariesDict:
                        ariesDict[date].append(values)
                    else:
                        ariesDict[date] = [values]
                    
            self.ariesDictionary = ariesDict
            return os.path.abspath(self.ariesFile)
        except:    
            raise ValueError("Fix.setAriesFile: The file violates the parameter rules")                    
    
    def setStarFile(self, starFile):
        if(starFile == None):
            raise ValueError("Fix.setStarFile: The file violates the parameter rules 1")                    
        
        checkForPeriod = starFile.find(".")
        if(checkForPeriod != -1):
            enteredFileType = starFile[checkForPeriod + 1: len(starFile)]
            if(enteredFileType != "txt"):
                raise ValueError("Fix.setStarFile: The file violates the parameter rules 2")                    
        else:
            raise ValueError("Fix.setStarFile: The file violates the parameter rules 3")                    
        
        try:
            self.starFile = starFile
            f = open(self.log, "a")
            f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Star file:\t" + os.path.abspath(self.starFile) + "\n")
        
            starDict = {}
            with open(starFile) as sf:
                for line in sf:
                    entry = line.split("\t", 1)
                    star = entry[0]
                    values = entry[1].split()
                    if star in starDict:
                        starDict[star].append(values)
                    else:
                        starDict[star] = [values]
                    
            self.starDictionary = starDict
            return os.path.abspath(self.starFile)
        except:    
            raise ValueError("Fix.setStarFile: The file violates the parameter rules 4")                    
    
    def getBody(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        bodyList = xmlDocument.getElementsByTagName('body')
        if(len(bodyList) == 0):
            self.errorCount += 1
            
        try:
            self.body = bodyList[count].firstChild.nodeValue
            return self.body
        except:
            self.errorCount += 1
            
    def getDate(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        dateList = xmlDocument.getElementsByTagName('date')
        self.date = dateList[count].firstChild.nodeValue
        try:
            datetime.strptime(self.dateNeededForGHA, "%m/%d/%y")
            datetime.strptime(self.date, "%Y-%m-%d")
            return self.date
        except:
            self.errorCount += 1
            
    def getTime(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        timeList = xmlDocument.getElementsByTagName('time')
        self.time = timeList[count].firstChild.nodeValue
        try:
            datetime.strptime(self.time, "%H:%M:%S")
            return self.time
        except:
            self.errorCount += 1
            
    def getObservation(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        observationList = xmlDocument.getElementsByTagName('observation')
        self.observation = observationList[count].firstChild.nodeValue
        strDelimiter = self.observation.find("d")
        if(strDelimiter == -1):
            self.errorCount += 1
        else:
            return self.observation
        
    def getHeight(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        heightList = xmlDocument.getElementsByTagName('height')
        if(len(heightList) == 0):
            self.numericHeight = 0.0
            return self.numericHeight
        
        self.height = heightList[count].firstChild.nodeValue        
        try:
            self.numericHeight = float(self.height)
            if(self.numericHeight <= 0):
                self.errorCount += 1
            else:    
                return self.numericHeight
        except:
            self.errorCount += 1
            
    def getTemp(self, count):
            xmlDocument = minidom.parseString(self.strOfSightingFile)
            tempList = xmlDocument.getElementsByTagName('temperature')
            if(len(tempList) == 0):
                self.intTemperature = 72
                return self.intTemperature
            
            self.temp = tempList[count].firstChild.nodeValue
            self.intTemperature = int(self.temp)
            if(self.intTemperature <= -20):
                self.errorCount += 1
            elif(self.intTemperature >= 120):
                self.errorCount += 1
            else:
                return self.intTemperature
            
    def getPressure(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        pressureList = xmlDocument.getElementsByTagName('pressure')
        if(len(pressureList) == 0):
            self.intPressure = 1010
            return self.intPressure
            
        self.pressure = pressureList[count].firstChild.nodeValue
        checkForPeriod = self.pressure.find(".")
        if(checkForPeriod != -1):
            raise ValueError("Fix.getSightings: The Pressure violates the parameter rules")
        else:
            self.intPressure = int(self.pressure)
            return self.intPressure
        
    def getHorizon(self, count):
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        horizonList = xmlDocument.getElementsByTagName('horizon')
        if(len(horizonList) == 0):
            self.horizon = "natural"
            return self.horizon
        
        self.horizon = horizonList[count].firstChild.nodeValue
        if(self.horizon.lower() == "natural"):
            return self.horizon
        elif(self.horizon.lower() == "artificial"):
            return self.horizon
        else:
            self.errorCount += 1
            
    def getGHA(self):
        # Use celestial body as key for the star dictionary. This will retrieve the values
        # needed for Note 4 on the requirements.
        # Use the date as key for the aries dictionary. This will retrieve the values needed
        # Once all values are retrieved we can compute the GHA
        bodyKey = self.body
        
            
    def getSightings(self):
        if(self.strOfSightingFile == None):
            raise ValueError("Fix.getSightings: Sighting file not set")
        if(self.ariesDictionary == None):
            raise ValueError("Fix.getSightings: Aries file not set")
        if(self.starDictionary == None):
            raise ValueError("Fix.getSightings: Star file not set")
        
        self.errorCount = 0
        self.totalErrorCount = 0
        xmlDocument = minidom.parseString(self.strOfSightingFile)
        sightingList = xmlDocument.getElementsByTagName('sighting')
        amount = len(sightingList)
        usedAngle = Angle.Angle()
        f = open(self.log, "a")
        for i in range(0, amount):
            self.dateNeededForGHA = None
            self.getBody(i)
            self.getDate(i)
            self.getHeight(i)
            self.getHorizon(i)
            self.getObservation(i)
            self.getPressure(i)
            self.getTemp(i)
            self.getTime(i)
            usedAngle.setDegreesAndMinutes(self.observation)
            altitude = usedAngle.getDegrees()
            if(self.horizon == "Natural"):
                self.dip = (-0.97 * sqrt(float(self.height))) / 60
            else:
                self.dip = 0
            self.refraction = (-0.00452 * self.intPressure) / (273 + ((5/9) * (self.intTemperature - 32))) / tan(altitude)
            self.adjustedAltitude = (tan(altitude)) + self.dip + self.refraction
            if(self.errorCount == 0):
                #self.getGHA()
                f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + self.body + "\t" + self.date + "\t" + self.time + "\t" + self.observation + "\n")
            else:
                self.totalErrorCount += 1
                self.errorCount = 0
                continue    
            
        f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Sighting errors:\t" + str(self.totalErrorCount))
        f.close()
        appLatitude = "0d0.0"
        appLongitude = "0d0.0"
        return (appLatitude, appLongitude)
  
    