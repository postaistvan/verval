from unittest import TestCase
from app.src.server import Fkondenz


class TestInsertDataBySensorID(TestCase):

	def test_insertDataBySensorID_inserted(self):
		fkond = Fkondenz(True)
		
		testData = 1
		testData1 = 2.6
		
		fkond.insertDataBySensorID(testData, testData1)
		
		self.assertTrue( (fkond.getTestData() == testData) and (fkond.getTestData1() == testData1) )
		
	def test_insertDataBySensorID_notInserted(self):
		fkond = Fkondenz(True)
		
		testData = 1
		testData1 = None
		
		fkond.insertDataBySensorID(testData, testData1)
		
		self.assertTrue( (fkond.getTestData() == testData) and (fkond.getTestData1() == None) )
		
	def test_insertDataBySensorID_notExistingId(self):
		fkond = Fkondenz(True)
		
		testData = -1
		testData1 = None
		
		fkond.insertDataBySensorID(testData, testData1)
		
		self.assertTrue( (fkond.getTestData() == testData) and (fkond.getTestData1() == None) )
		
