import unittest
from bootstrap.app import create_app

class HttpTest(unittest.TestCase):
    def setUp(self):
        """Setup test environment."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_homepage_returns_200(self):
        """Test apakah halaman utama dapat diakses."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Selamat Datang', response.data)

    def tearDown(self):
        """Clean up after test."""
        pass

if __name__ == '__main__':
    unittest.main()