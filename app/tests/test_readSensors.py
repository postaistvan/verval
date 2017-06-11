from unittest import TestCase
from app.src.server import Fkondenz


class TestReadSensors(TestCase):

	def test_readSensors_type(self):
		fkond = Fkondenz(True)
		
		fkond.setTestData(1)
		fkond.setTestData(1)
		fkond.setTestData(1)
        
		self.assertEqual(type(fkond.readSensors()), tuple)

	def test_readSensors_is_not_None(self):
		fkond = Fkondenz(True)
		
		fkond.setTestData(1)
		fkond.setTestData(1)
		fkond.setTestData(1)
        
		self.assertTrue(fkond.readSensors() is not None)

	def test_readSensors_is_none(self):
		fkond = Fkondenz(True)
		
		fkond.setTestData(None)
		fkond.setTestData(None)
		fkond.setTestData(None)
		
		self.assertTrue(fkond.readSensors() == (None, None, None))
