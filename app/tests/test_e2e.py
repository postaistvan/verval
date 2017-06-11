from unittest import TestCase
from app.src.server import Fkondenz
from dweet import Dweet


class TestE2E(TestCase):

	def test_e2e_readSensors_sendToDweet(self):
		fkond = Fkondenz(True)
		dweet = Dweet()
		
		testData = 1
		testData1 = 2
		testData2 = 3
		
		fkond.setTestData(testData)
		fkond.setTestData(testData1)
		fkond.setTestData(testData2)
		
		testData_, testData1_, testData2_ = fkond.readSensors()
        
		fkond.uploadToDweet(testData_, testData1_, testData2_)
				
		self.assertEqual(fkond.getTestData(), "Uploaded")
