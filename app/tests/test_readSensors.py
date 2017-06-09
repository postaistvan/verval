from unittest import TestCase

from app.src.server import readSensors


class TestReadSensors(TestCase):
    response = readSensors()

    def test_readSensors_type(self):
        self.assertEqual(type(TestReadSensors.response), tuple)

    def test_readSensors_is_not_None(self):
        self.assertTrue(TestReadSensors.response is not None)

    def test_readSensors_is_null(self):
        self.assertTrue(TestReadSensors.response == (0, 0, 0))
