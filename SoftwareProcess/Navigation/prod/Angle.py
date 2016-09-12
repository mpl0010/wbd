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
        pass
    
    def setDegrees(self, degrees):
        #returns the resulting angle as degrees
        if(isinstance(degrees, float)):
            self.angle = self.angle + (degrees % 360)
            return self.angle
        elif(isinstance(degrees, int)):
            self.angle = self.angle + (degrees % 360)
            return self.angle
        else:
            raise ValueError("Angle.setDegrees: The value needs to be an instance of a float.")
        pass
    
    def setDegreesAndMinutes(self, degrees):
        if(isinstance(degrees, basestring)):
            index = degrees.index("d")
            firstHalf = degrees[0:index]
            secondHalf = degrees[index + 1: len(degrees)]
            try:
                invalidAngle1 = int(firstHalf)
                invalidAngle2 = float(secondHalf)
            except ValueError:
                #handle exception
                print "The value must resemble this structure (degree)d(Minutes)"
        
            minuteConvert = float(secondHalf) / 60.0
            #Correcting the degree if greater than 360 or less than 0
            tempFirstHalf = int(firstHalf) % 360
            self.angle = round(tempFirstHalf + minuteConvert, 1)
            return self.angle
            
        else:
            raise ValueError("Angle.setDegreesAndMinutes: The value needs to be an instance of a string.")
        pass
    
    def add(self, angle):
        #Adds two angles
        result = round((self.angle + angle.angle) % 360, 1)
        return result
        pass
    
    def subtract(self, angle):
        #Subtract two angles
        result = round((self.angle - angle.angle) % 360, 1)
        return result
        pass
    
    def compare(self, angle):
        #Compare two angles
        if(self.angle > angle.angle):
            return 1
        elif(self.angle < angle.angle):
            return -1
        else:
            return 0
        pass
    
    def getString(self):
        stringAngle = str(self.angle)
        degree = stringAngle[0:stringAngle.index(".")]
        minutes = stringAngle[stringAngle.index(".") + 1: len(stringAngle)]
        minutesConverted = round(float(minutes) * 60.0, 1)
        return degree + "d" + str(minutesConverted)
        pass
    
    def getDegrees(self):
        #Returns the angle
        return self.angle
        pass