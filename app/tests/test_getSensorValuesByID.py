from unittest import TestCase
from app.src.server import Fkondenz


class TestGetSensorValuesByID(TestCase):

	def test_getSensorValuesByID_hasData(self):
		fkond = Fkondenz(True)
		
		testData = [ ("2016-01-01", 2.2) ] 
		fkond.setTestData(testData)
		
		self.assertTrue(fkond.getSensorValuesByID(1) == [ ("2016-01-01", 2.2) ])

	def test_getSensorValuesByID_emptyData(self):
		fkond = Fkondenz(True)
		
		testData = [] 
		fkond.setTestData(testData)
		
		self.assertTrue(fkond.getSensorValuesByID(1) == [])

	def test_getSensorValuesByID_none(self):
		fkond = Fkondenz(True)
		
		testData = None
		fkond.setTestData(testData)
		
		self.assertTrue(fkond.getSensorValuesByID(-1) == None)