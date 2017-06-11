from unittest import TestCase
from app.src.server import Fkondenz


class TestGetSensorLastValueByID(TestCase):

	def test_getSensorLastValueByID_true(self):
        # Fkondenz a testData-t fogja hasznalni, megszuntetve a fuggosegeket
		fkond = Fkondenz(True)
		
		testData = "2016-01-01"
		testData1 = 2.6
		
		fkond.setTestData(testData)
		fkond.setTestData1(testData1)
		
		self.assertTrue(fkond.getSensorLastValueByID(1) == (testData, testData1))
		
	def test_getSensorLastValueByID_false(self):
		# Fkondenz a testData-t fogja hasznalni, megszuntetve a fuggosegeket
		fkond = Fkondenz(True)
		
		testData = "2016-01-01"
		testData1 = 2.6
		
		fkond.setTestData(testData)
		fkond.setTestData1(testData1)
		
		self.assertFalse(fkond.getSensorLastValueByID(1) == (testData, 1.1))
		
	def test_getSensorLastValueByID_none(self):
		# Fkondenz a testData-t fogja hasznalni, megszuntetve a fuggosegeket
		fkond = Fkondenz(True)
		
		testData = None
		testData1 = None
		
		fkond.setTestData(testData)
		fkond.setTestData1(testData1)
		
		self.assertTrue(fkond.getSensorLastValueByID(-1) == (None, None))