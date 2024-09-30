# test_search_routes.py
import unittest
from flask import json
from test_base import BaseTestCase  # Import the base test class
from app.models import Unit, Course, Specialisation, db

class TestSearchRoutes(BaseTestCase):
    def insert_mock_data(self):
        """Override insert_mock_data if needed, or use existing setup data from BaseTestCase."""
        # Add mock data for Unit search
        unit1 = Unit(name='Data Structures', code='CS201')
        unit2 = Unit(name='Software Testing', code='CS301')
        db.session.add_all([unit1, unit2])

        # Add mock data for Course search
        course1 = Course(title='Computer Science', code='CS101', description='Computer Science Course')
        course2 = Course(title='Software Engineering', code='SE101', description='Software Engineering Course')
        db.session.add_all([course1, course2])

        # Add mock data for Specialisation search
        specialisation1 = Specialisation(name='Artificial Intelligence', code='AI101', description='AI Specialisation')
        specialisation2 = Specialisation(name='Cyber Security', code='CS201', description='Cyber Security Specialisation')
        db.session.add_all([specialisation1, specialisation2])

        # Commit the changes
        db.session.commit()

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
        response = self.client.get('/search_specialisations?query=Artificial')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], 'Artificial Intelligence')

        # Search for 'Cyber' in specialisations
        response = self.client.get('/search_specialisations?query=Cyber')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], 'Cyber Security')

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
        response = self.client.get('/search?query=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No units should be returned

        response = self.client.get('/search_courses?query=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No courses should be returned

        response = self.client.get('/search_specialisations?query=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)  # No specialisations should be returned

if __name__ == '__main__':
    unittest.main()
