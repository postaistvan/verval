from unittest import TestCase
from app.src.server import Fkondenz


class TestReadDht(TestCase):

	def test_readDht_true(self):
		fkond = Fkondenz(True)
		
		testData = 1.7
		testData1 = 2.6
		
		fkond.setTestData(testData)
		fkond.setTestData1(testData1)
		
		fkond.readDht()
		
		self.assertTrue( (fkond.getTestData() == 1.7) and (fkond.getTestData1() == 2.6) )
		
	def test_readDht_none(self):
		fkond = Fkondenz(True)
		
		testData = None
		testData1 = None
		
		fkond.setTestData(testData)
		fkond.setTestData1(testData1)
		
		fkond.readDht()
		
		self.assertTrue( (fkond.getTestData() == None) and (fkond.getTestData1() == None) )