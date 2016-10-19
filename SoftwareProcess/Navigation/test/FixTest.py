import unittest
import Navigation.prod.Fix as Fix

class FixTest(unittest.TestCase):
    def setUp(self):
        self.className = "Fix."
    def tearDown(self):
        pass
    
#    Acceptance Test: 100
#        Analysis - Contructor
#            inputs
#                logFile to which celestial navigation calculations are written
#            outputs
#                An instance of Fix
#            state change
#                Writes the following entry to the logFile
#                    Start of log
#
#            Happy path
#                nominal case:  Fix()
#            Sad path
#                File name violates the parameter rules: Must be a String
#                File name violates the parameter rules: Can only be a txt file

#Happy path
    def test100_010_ShouldCreateInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix(), Fix.Fix)
        
#Sad Path
    def test100_110_ShouldRaiseExceptionNonString(self):
        expectedString = "Fix.__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.Fix(123)                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test100_120_ShouldRaiseExceptionNonTxtFile(self):
        expectedString = "Fix.__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.Fix("hello.dxx")                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
#-----------------------------------------------------------------
#    Acceptance Test: 200
#        Analysis - setSightingFile
#            inputs
#                sightingFile - file that contains XML descriptions of navigational sightings
#            outputs
#                A string having the value passed as the "sightingFile"
#            state change
#                Writes the following entry to the log file:
#                    Start of sighting file f.xml
#                        --where f.xml is the actual name of the file
#
#            Happy path
#                nominal case: returns a string value
#            Sad path
#                not an xml file: setSightingFile("f.txt")
#                not a string: setSightingFile(123)
#
#    Happy path
    def test200_010_ShouldReturnTheStringValue(self):
        expectedString = "<fix>\n<sighting>\n<body>Aldebaran</body>\n<date>2016-03-01</date>\n<time>23:40:01</time>\n<observation>015d04.9</observation>\n<height>6.0</height>\n<temperature>72</temperature>\n<pressure>1010</pressure>\n<horizon>Artificial</horizon>\n</sighting>\n<sighting>\n<body>Peacock</body>\n<date>2016-03-02</date>\n<time>00:05:05</time>\n<observation>045d15.2</observation>\n<height>6.0</height>\n<temperature>71</temperature>\n<pressure>1010</pressure>\n<horizon>Natural</horizon>\n</sighting>\n</fix>"
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        self.assertEquals(expectedString, theFix.strOfSightingFile)
        
#    Sad path
    def test_200_110_ShoudRaiseErrorForNonXMLFile(self):
        expectedString = "Fix.setSightingFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("Hello.txt")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    def test_200_120_ShouldRaiseErrorForNonString(self):
        expectedString = "Fix.setSightingFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(123)                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
