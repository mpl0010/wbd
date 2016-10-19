'''
    Created for the use of astronavigation that calculates our location based on celestial bodies.
    Baselined: 11 Sep2016
    Modified: 11 Sep2016
    @author: M. Lloyd
'''

class Angle():
    def __init__(self):
        #self.angle = ...       set to 0 degrees 0 minutes
        #creates an instance of Angle.
        self.angle = 0.0
    
    def setDegrees(self, degrees = 0):
        #returns the resulting angle as degrees
        try:
            self.angle = self.angle + (float(degrees) % 360)
            return self.angle
        except:
            raise ValueError("Angle.setDegrees: degrees violates the parameter specifications")
    
    def setDegreesAndMinutes(self, degrees):
        if(isinstance(degrees, basestring)):
            strDelimiter = degrees.find("d")
            strDecimalLength = degrees.find(".")
            firstHalf = degrees[0:strDelimiter]
            secondHalf = degrees[strDelimiter + 1: len(degrees)]
            decimalPlacesAmount = degrees[strDecimalLength + 1: len(degrees)]
            if(strDelimiter == -1):
                raise ValueError("Angle.setDegreesAndMinutes: The value must resemble this structure (degree)d(Minutes)")
            elif((strDecimalLength != -1) & (len(decimalPlacesAmount) != 1)):
                raise ValueError("Angle.setDegreesAndMinutes: The Minutes value can only have one decimal place")
            else:
                try:
                    if(float(secondHalf) < 0.0):
                        raise ValueError("Angle.setDegreesAndMinutes: The Minute value must be positive")
                    else:
                        tempFirstHalf = int(firstHalf) % 360
                        minuteConvert = float(secondHalf) / 60.0
                        self.angle = tempFirstHalf + minuteConvert
                        return self.angle
            
                except:
                #handle exception
                    raise ValueError("Angle.setDegreesAndMinutes: The value must resemble this structure (degree)d(Minutes)")
                    
            #Correcting the degree if greater than 360 or less than 0
        else:
            raise ValueError("Angle.setDegreesAndMinutes: The value needs to be an instance of a string.")
    
    def add(self, angle = None):
        if(angle == None):
            raise ValueError("Angle.add: An angle value must be passed in")
        elif(isinstance(angle, Angle)):
            self.angle = (self.angle + angle.angle) % 360
            return self.angle
        else:
            raise ValueError("Angle.add: An angle value must be passed in")

    def subtract(self, angle = None):
        #Subtract two angles
        if(angle == None):
            raise ValueError("Angle.subtract: An angle value must be passed in")
        elif(isinstance(angle, Angle)):
            self.angle = (self.angle - angle.angle) % 360
            return self.angle
        else:
            raise ValueError("Angle.subtract: An angle value must be passed in")
    
    def compare(self, angle = None):
        #Compare two angles
        if(angle == None):
            raise ValueError("Angle.compare: angle is not a valid instance of Angle")
        elif(isinstance(angle, Angle)):
            if(self.angle > angle.angle):
                return 1
            elif(self.angle < angle.angle):
                return -1
            else:
                return 0
        else:
            raise ValueError("Angle.compare: angle is not a valid instance of Angle")
    
    def getString(self):
        strAngle = str(self.angle)
        degree = strAngle[0:strAngle.find(".")]
        degreeConverted = int(degree) % 360
        minutes = strAngle[strAngle.find(".") + 1: len(strAngle)]
        print minutes
        minutesConverted = float(minutes) * 6
        return str(degreeConverted) + "d" + str(minutesConverted)
    
    def getDegrees(self):
        #Returns the angle
        return self.angle 