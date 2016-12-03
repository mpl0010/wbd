'''
    Created for the use of astronavigation that calculates our location based on celestial bodies.
    Baselined: 11 Sep2016
    Modified: 11 Sep2016
    @author: M. Lloyd
'''

from decimal import *

class Angle():
    def __init__(self):
        #self.angle = ...       set to 0 degrees 0 minutes
        #creates an instance of Angle.
        self.angle = 0.0
    
    def setDegrees(self, degrees = 0.0):
        #returns the resulting angle as degrees
        try:
            self.angle = (float(degrees) % 360.0)
            degree = int(self.angle)
            minutes = round((self.angle - degree)*60, 1)
            self.angle = degree + minutes/60.0
            return self.angle
        except:
            raise ValueError("Angle.setDegrees: degrees violates the parameter specifications")
    
    def setDegreesAndMinutes(self, degrees):
        try:
            angStr = degrees.split("d")
            if (float(angStr[1]) < 0.0):
                raise ValueError("Angle.setDegreesAndMinutes: The Minutes value can only have one decimal place")
    
            decimalCheck = abs(Decimal(angStr[1]).as_tuple().exponent)
            if (decimalCheck > 1):
                raise ValueError("Angle.setDegreesAndMinutes: The Minutes value can only have one decimal place")
            
            firstHalf = int(angStr[0])
            secondHalf = float(angStr[1]) / 60.0
            
            if (-360 < firstHalf < 0):
                self.angle = 360 - (abs(firstHalf) + secondHalf)
            else:
                self.angle = (firstHalf % 360) + secondHalf
                
            return self.angle
        except:
            raise ValueError("Angle.setDegreesAndMinutes: The Minutes value can only have one decimal place")
        
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
        strAngleDeg = str(int(self.angle) // 1)
        strAngleMin = str(round(((self.angle % 1) * 60.0), 1))
        return strAngleDeg + "d" + strAngleMin
    
    def getDegrees(self):
        #Returns the angle
        self.angle = self.angle % 360
        return self.angle 