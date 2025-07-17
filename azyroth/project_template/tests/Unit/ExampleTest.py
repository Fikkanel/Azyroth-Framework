import unittest

class ExampleTest(unittest.TestCase):

    def test_true_is_true(self):
        """Contoh unit test sederhana."""
        self.assertTrue(True)
        
    def test_addition(self):
        """Test fungsi penambahan dasar."""
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()