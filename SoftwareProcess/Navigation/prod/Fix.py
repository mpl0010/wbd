from datetime import datetime, timedelta
from xml.dom import minidom
import math
from decimal import *
import Angle
from math import tan, sqrt, pi, sin
import os

class Fix():
    def __init__(self, logFile = "log.txt"):
        try:
            self.log = logFile
            self.sightingFile = None
            self.strOfSightingFile = None
            self.starDictionary = None
            self.ariesDictionary = None
            self.ariesFile = None
            self.starFile = None
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
                return os.path.abspath(self.sightingFile)
            except:    
                raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
        else:
            raise ValueError("Fix.setSightingFile: The file violates the parameter rules")                    
             
    def setAriesFile(self, ariesFile = None):
        if(ariesFile == None):
            raise ValueError("Fix.setAriesFile: The file violates the parameter rules")                    
        if(isinstance(ariesFile, basestring)):
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
        else:
            raise ValueError("Fix.setAriesFile: The file violates the parameter rules")
    
    def setStarFile(self, starFile = None):
        if(starFile == None):
            raise ValueError("Fix.setStarFile: The file violates the parameter rules 1")                    
        if(isinstance(starFile, basestring)):
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
        else:
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
            self.dateNeededForGHA = self.date
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
            self.errorCount += 1
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
        sightingDate = self.date
        convertedDate = self.dateNeededForGHA
        convertedDate = datetime.strptime(convertedDate,"%Y-%m-%d").strftime("%m/%d/%y")
        convertedDate = datetime.strptime(convertedDate,"%m/%d/%y")
        ariesDate = datetime.strptime(sightingDate, "%Y-%m-%d").strftime("%m/%d/%y")
        sightingBody = self.body
        timeArray = self.time.split(":") 
        hourNeeded = int(timeArray[0])
        s = int(timeArray[1]) * 60 + int(timeArray[2])
        starDictionary = self.starDictionary
        ariesDictionary = self.ariesDictionary
        starIndex = 0
        geoPosLatAngle = Angle.Angle()
        geoPosLonAngle = Angle.Angle()
        starSarHourAngle = Angle.Angle()
        ariesGHA2Angle = Angle.Angle()
        ariesGHA1Angle = Angle.Angle()
        ariesGHA = Angle.Angle()
        
        for star in starDictionary[sightingBody]:
            checkDate = datetime.strptime(star[0], "%m/%d/%y")
            if (checkDate == convertedDate):
                observedStar = starDictionary[sightingBody][starIndex]
                break
            elif (checkDate > convertedDate):
                observedStar = starDictionary[sightingBody][starIndex - 1]
                break
        

        
        geographicPositionLatitude = observedStar[2]
        geoPosLatAngle.setDegreesAndMinutes(geographicPositionLatitude)
        starSHA = observedStar[1]
        returnedSHA = observedStar[2]
        returnedSHAANlge = Angle.Angle()
        returnedSHAANlge.setDegreesAndMinutes(returnedSHA)
        starSarHourAngle.setDegreesAndMinutes(starSHA)
        
        dateList = ariesDictionary[ariesDate]
        aries1GHA = dateList[hourNeeded][1]
        
        if (hourNeeded == 23):
            ariesDate = datetime.strptime(ariesDate, "%m/%d/%y")
            ariesDate += timedelta(days=1)
            ariesDate = datetime.strftime(ariesDate, "%m/%d/%y")
            dateList = ariesDictionary[ariesDate]
            aries2GHA = dateList[0][1]
        else:
            aries2GHA = dateList[hourNeeded + 1][1]

        ariesGHA1Angle.setDegreesAndMinutes(aries1GHA)
        ariesGHA2Angle.setDegreesAndMinutes(aries2GHA)
        part1 = float(ariesGHA1Angle.angle)
        part2 = float(ariesGHA2Angle.angle)

        computeFormula = abs(part2 - part1)
        computeFormula = float(computeFormula) * s/3600
        ariesGHA.setDegrees(computeFormula)
        ariesGHA.add(ariesGHA1Angle)
        
        ariesGHA.add(starSarHourAngle)
        
        
        
        geoPosLonAngle.setDegrees((ariesGHA.angle) % 360)
        self.latitude = returnedSHAANlge.getDegrees()
        self.longitude = geoPosLonAngle.getDegrees()
        return (returnedSHA, geoPosLonAngle)
        
            
    def getSightings(self, assumedLatitude = "0d0.0", assumedLongitude = "0d0.0"):
        if(self.strOfSightingFile == None):
            raise ValueError("Fix.getSightings: Sighting file not set")
        if(self.ariesDictionary == None):
            raise ValueError("Fix.getSightings: Aries file not set")
        if(self.starDictionary == None):
            raise ValueError("Fix.getSightings: Star file not set")
        if(not(isinstance(assumedLatitude, basestring))):
            raise ValueError("Fix.getSightings: assumedLatitude not string")
        if(not(isinstance(assumedLongitude, basestring))):
            raise ValueError("Fix.getSightings: assumedLongitude not string")
        try:
            checkStrLat = assumedLatitude.split("d")
            if (float(checkStrLat[1]) < 0.0):
                raise ValueError("Fix.getSightings: The parameters are illegal")
    
            decimalCheck = abs(Decimal(checkStrLat[1]).as_tuple().exponent)
            if (decimalCheck > 1):
                raise ValueError("Fix.getSightings: The parameters are illegal")
            
            checkStrLon = assumedLongitude.split("d")
            if (float(checkStrLon[1]) < 0.0):
                raise ValueError("Fix.getSightings: The parameters are illegal")
    
            decimalCheck = abs(Decimal(checkStrLon[1]).as_tuple().exponent)
            if (decimalCheck > 1):
                raise ValueError("Fix.getSightings: The parameters are illegal")
        except:
            raise ValueError("Fix.getSightings: The parameters are illegal")
        
        checkForLatN = assumedLatitude.find("N")
        checkForLatS = assumedLatitude.find("S")
        if (checkForLatN == -1):
            if (checkForLatS == -1):
                assumedLatitude = "0d0.0"
                print assumedLatitude
            else:
                assumedLatitude = "-" + assumedLatitude[1:]
                print assumedLatitude
        else:
            assumedLatitude = assumedLatitude[1:]
            print assumedLatitude
            
        
        self.errorCount = 0
        self.totalErrorCount = 0
        self.sumCosAzimuth = 0
        self.sumSinAzimuth = 0
        self.sumDistance = 0
        self.multCosVar = 0
        self.multSinVar = 0
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
            observedAltitude = usedAngle.setDegreesAndMinutes(self.observation)
            if(self.errorCount == 0):
                #self.getGHA()
                if(self.horizon.lower() == "natural"):
                    self.dip = float((-0.97 * sqrt(float(self.numericHeight))) / 60.0)
                else:
                    self.dip = 0.0
                self.refraction = (-0.00452 * self.intPressure) / (273 + (.5556 * (self.intTemperature - 32))) / tan(observedAltitude * pi/180)
                self.adjustedAltitude = round(observedAltitude + self.dip + self.refraction, 3)
                usedAngle.angle = self.adjustedAltitude
                (lat, lon) = self.getGHA()

                assumedLonAngle = Angle.Angle()
                assumedLatAngle = Angle.Angle()
                assumedLatAngle.setDegreesAndMinutes(assumedLatitude)
                assumedLonAngle.setDegreesAndMinutes(assumedLongitude)
                
                LHA = self.longitude - assumedLonAngle.getDegrees()
                
                correctedAltitude = math.asin((math.sin(self.latitude) * math.sin(assumedLatAngle.getDegrees()))) + (math.cos(self.latitude) * math.cos(assumedLatAngle.getDegrees()) * math.cos(LHA))
                distanceAdjustment = round(usedAngle.getDegrees() - correctedAltitude, 1)
                azimuthAdjustment = math.acos(math.sin(self.latitude) - math.sin(assumedLatAngle.getDegrees()) * (math.cos(assumedLatAngle.getDegrees()) * math.cos(distanceAdjustment)))
                self.sumDistance += distanceAdjustment
                self.sumCosAzimuth += math.cos(azimuthAdjustment)
                self.sumSinAzimuth += math.sin(azimuthAdjustment)
                self.multCosVar += self.sumDistance * self.sumCosAzimuth 
                self.multSinVar += self.sumDistance * self.sumSinAzimuth
                
                f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + self.body + "\t" + self.date + "\t" + self.time + "\t" + usedAngle.getString() + "\t" + str(lat) + "\t" + str(lon.getString()) + "\t" + str(assumedLatitude) + "\t" + str(assumedLongitude) + "\t" + str(azimuthAdjustment) + "\t" + str(round(distanceAdjustment), 1) +"\n")

            else:
                self.totalErrorCount += 1
                self.errorCount = 0
            
        f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Sighting errors:\t" + str(self.totalErrorCount) + "\n")
        
        latDegrees = assumedLatAngle.getDegrees()    
        degreesLatitude = latDegrees + (self.multCosVar / 60)
        assumedLatAngle.setDegrees(degreesLatitude)
        approximateLatitude = assumedLatAngle.getString()
        
        lonDegrees = assumedLonAngle.getDegrees()    
        degreesLongitude = lonDegrees + (self.multSinVar / 60)
        assumedLonAngle.setDegrees(degreesLongitude)
        approximateLongitude = assumedLonAngle.getString()
        
        f.write("LOG: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "-6:00\t" + "Approximate latitude:\t" + approximateLatitude + "\t" + "Approximate Longitude:\t" + approximateLongitude)
        return (approximateLatitude, approximateLongitude)
        f.close()
    