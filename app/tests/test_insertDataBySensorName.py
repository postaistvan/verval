from unittest import TestCase
from app.src.server import Fkondenz


class TestInsertDataBySensorName(TestCase):

	def test_insertDataBySensorName_humidity_true(self):
		fkond = Fkondenz(True)
		
		testData = "Humidity"
		testData1 = 2.6
		
		fkond.insertDataBySensorName(testData, testData1)
		
		self.assertTrue( (fkond.getTestData() == "Humidity") and (fkond.getTestData1() == 2.6) )
		
	def test_insertDataBySensorName_temperature_true(self):
		fkond = Fkondenz(True)
		
		testData = "Temperature"
		testData1 = 2.6
		
		fkond.insertDataBySensorName(testData, testData1)
		
		self.assertTrue( (fkond.getTestData() == "Temperature") and (fkond.getTestData1() == 2.6) )
		
	def test_insertDataBySensorName_distance_true(self):
		fkond = Fkondenz(True)
		
		testData = "Distance"
		testData1 = 2
		
		fkond.insertDataBySensorName(testData, testData1)
		
		self.assertTrue( (fkond.getTestData() == "Distance") and (fkond.getTestData1() == 2) )

	def test_insertDataBySensorName_distance_true(self):
		fkond = Fkondenz(True)
		
		testData = "NotExisting"
		testData1 = None
		
		fkond.insertDataBySensorName(testData, testData1)
		
		self.assertTrue( (fkond.getTestData() == "NotExisting") and (fkond.getTestData1() == None) )
