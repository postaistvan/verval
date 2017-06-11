from unittest import TestCase
from app.src.server import Fkondenz


class TestGetSensorTypeByName(TestCase):

	# Humidity ID in the database is 1
	def test_getSensorTypeByName_humidity_true(self):

		fkond = Fkondenz(True)
		
		testData = 1
		fkond.setTestData(testData)
		
		self.assertTrue(fkond.getSensorTypeByName("Humidity") == 1)

	# Temperature ID in the database is 2
	def test_getSensorTypeByName_temperature_true(self):

		fkond = Fkondenz(True)
		
		testData = 2
		fkond.setTestData(testData)
		
		self.assertTrue(fkond.getSensorTypeByName("Temperature") == 2)

	# Distance ID in the database is 3
	def test_getSensorTypeByName_distance_true(self):

		fkond = Fkondenz(True)
		
		testData = 3
		fkond.setTestData(testData)
		
		self.assertTrue(fkond.getSensorTypeByName("Distance") == 3)	
		
	# Humidity ID in the database is 1
	def test_getSensorTypeByName_humidity_false(self):

		fkond = Fkondenz(True)
		
		testData = 0
		fkond.setTestData(testData)
		
		self.assertFalse(fkond.getSensorTypeByName("Humidity") == 1)

	# Temperature ID in the database is 2
	def test_getSensorTypeByName_temperature_false(self):

		fkond = Fkondenz(True)
		
		testData = 0
		fkond.setTestData(testData)
		
		self.assertFalse(fkond.getSensorTypeByName("Temperature") == 2)

	# Distance ID in the database is 3
	def test_getSensorTypeByName_distance_false(self):

		fkond = Fkondenz(True)
		
		testData = 0
		fkond.setTestData(testData)
		
		self.assertFalse(fkond.getSensorTypeByName("Distance") == 3)
		
	# The asked sensor name is not existing in the database
	def test_getSensorTypeByName_distance_none(self):

		fkond = Fkondenz(True)
		
		testData = None
		fkond.setTestData(testData)
		
		self.assertTrue(fkond.getSensorTypeByName("NotExisting") == None)