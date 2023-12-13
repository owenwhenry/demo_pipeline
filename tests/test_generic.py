import unittest
import pipelines.generic

class test_generic(unittest.TestCase):

    def setUp(self):
        self.generic = pipelines.generic.GenericPipe

    def test_pull(self):
        with self.assertRaises(NotImplementedError):
            self.generic.pull()
    def test_validate(self):
        with self.assertRaises(NotImplementedError):
            self.generic.validate("some data")
    def test_map(self):
        with self.assertRaises(NotImplementedError):
            self.generic.map("some data")
    def test_push(self):
        with self.assertRaises(NotImplementedError):
            self.generic.push("some data")
    
class test_genericCDG(unittest.TestCase):

    def setUp(self):
        self.genericCDG = pipelines.generic.GenericCDGPipe()

    def test_init(self):
        self.assertEqual(
            self.genericCDG._url_base,
            "https://api.congress.gov/v3"
            )

