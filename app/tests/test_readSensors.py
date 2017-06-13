from unittest import TestCase

from app.src.server import Sensor


class TestReadSensors(TestCase):

    def test_readSensors_type(self):
        sensor = Sensor(database=None)
        self.assertEqual(type(sensor.readSensors()), tuple)

    def test_readSensors_is_not_None(self):
        sensor = Sensor(database=None)
        self.assertTrue(sensor.readSensors() is not None)

    def test_readSensors_is_null(self):
        sensor = Sensor(database=None)
        self.assertTrue(sensor.readSensors() == (0, 0, 0))
