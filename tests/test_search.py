import unittest
from flask import json
from test_base import BaseTestCase  # Import the base test class

class TestSearchRoutes(BaseTestCase):

    def test_search_units(self):
        """Test the /search route for units."""
        # Search for 'Data' in units
        response = self.client.get('/search?query=Data')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], 'Data Structures')

        # Search for 'Software' in units
        response = self.client.get('/search?query=Software')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], 'Software Testing')

        # Search for 'Algorithms' in units
        response = self.client.get('/search?query=Algorithms')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], 'Algorithms')

    def test_search_courses(self):
        """Test the /search_courses route."""
        # Search for 'Computer' in courses
        response = self.client.get('/search_courses?query=Computer')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['title'], 'Computer Science')

        # Search for 'Engineering' in courses
        response = self.client.get('/search_courses?query=Engineering')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['title'], 'Software Engineering')

    def test_search_specialisations(self):
        """Test the /search_specialisations route."""
        # Search for 'Artificial' in specialisations
        response = self.client.get('/search_specialisations?query=AI')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], 'AI Specialisation')

        # Search for 'Software Development' in specialisations
        response = self.client.get('/search_specialisations?query=Software Development')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], 'Software Development Specialisation')

    def test_search_no_results(self):
        """Test that an unmatched query returns no results."""
        # Search for 'Nonexistent' in all search routes
        response = self.client.get('/search?query=Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No units should match

        response = self.client.get('/search_courses?query=Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No courses should match

        response = self.client.get('/search_specialisations?query=Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No specialisations should match

    def test_search_empty_query(self):
        """Test that an empty query returns no results."""
        # Test empty query in all search routes
        response = self.client.get('/search?query=" "')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No units should be returned

        response = self.client.get('/search_courses?query=" "')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No courses should be returned

        response = self.client.get('/search_specialisations?query=" "')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No specialisations should be returned

if __name__ == '__main__':
    unittest.main()
