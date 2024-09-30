# test_welcome_page.py
import unittest
from test_base import BaseTestCase

class TestWelcomePage(BaseTestCase):
    def test_welcome_page_loads(self):
        """Test if the welcome page loads successfully."""
        response = self.client.get('/')  # Simulate a GET request to the welcome page
        self.assertEqual(response.status_code, 200)  # Check if the response is successful

    def test_welcome_page_content(self):
        """Test if the welcome page contains expected content."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if the response data contains specific text/content
        self.assertIn(b'Welcome To The Unit Set Builder App', response.data)
        self.assertIn(b'Curriculum Mapping', response.data)

    def test_welcome_page_button(self):
        """Test if the welcome page has a button to navigate to the next page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if the response data contains the button with the correct link
        self.assertIn(b'class="home-button-links"', response.data)   # Make sure the button/link has the correct ID

        response = self.client.get('/select-course', follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Final destination should have status 200
        self.assertIn(b'SELECT COURSE', response.data)

if __name__ == '__main__':
    unittest.main()
