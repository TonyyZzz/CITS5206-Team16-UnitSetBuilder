# test_base.py
import unittest
from app import create_app, db  # Replace 'app' with the name of your Flask app package
from flask_bcrypt import Bcrypt
from flask_login import login_user
from app.models import User, Course, UnitSet, Specialisation, Group, GroupElement, Unit, CourseSpecialisation

bcrypt = Bcrypt()

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Executed before each test method."""
        # Set up the database and insert mock data
        self.app = create_app(config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.insert_mock_data()
        self.create_test_user()
        self.login()

    def tearDown(self):
        """Executed after each test method."""
        # Remove the database session and drop all tables
        db.session.remove()    # Remove the session

        # Drop all tables to clean up the database
        db.drop_all()
        self.app_context.pop()



    def login(self):
        """Helper method to log in the test user before each test."""
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/login', json=login_data)
        self.assertEqual(response.status_code, 200)  # Ensure login was successful

    def create_test_user(self):
        """Insert a test user for login."""
        # Create a test user with a hashed password
        password_hash = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        user = User(username='testuser', email='testuser@example.com', password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

    def insert_mock_data(self):
        """Insert initial data for testing purposes."""

        # Create test courses
        course_cs = Course(title='Computer Science', code='CS101', description='Intro to Computer Science')
        course_se = Course(title='Software Engineering', code='SE101', description='Intro to Software Engineering')
        db.session.add(course_cs)
        db.session.add(course_se)
        db.session.commit()  # Commit the courses to the database so their IDs are generated


        # Create unit sets
        unit_set_cs = UnitSet(title='Core CS Units', description='Core units for CS', note='Required', course_id=course_cs.id)
        unit_set_se = UnitSet(title='Core SE Units', description='Core units for SE', note='Required', course_id=course_se.id)
        db.session.add(unit_set_cs)
        db.session.add(unit_set_se)


        # Create specialisations
        specialisation_ai = Specialisation(name='AI Specialisation', code='AI101', description='Artificial Intelligence focus', note='AI Track')
        specialisation_sd = Specialisation(name='Software Development Specialisation', code='SD101', description='Software Development focus', note='SD Track')
        db.session.add(specialisation_ai)
        db.session.add(specialisation_sd)

        # Create units
        unit_data_structures = Unit(name='Data Structures', code='CS102', description='Learn about Data Structures', credit_points=6)
        unit_algorithms = Unit(name='Algorithms', code='CS103', description='Learn about Algorithms', credit_points=6)
        unit_testing = Unit(name='Software Testing', code='SE102', description='Learn about Software Testing', credit_points=6)
        db.session.add(unit_data_structures)
        db.session.add(unit_algorithms)
        db.session.add(unit_testing)
        db.session.commit()  # Commit the courses to the database so their IDs are generated

        # Create groups
        group_cs_core = Group(group_type='Core', note='Core CS Group', unit_set_id=unit_set_cs.id)
        group_se_elective = Group(group_type='Elective', note='SE Elective Group', unit_set_id=unit_set_se.id)
        db.session.add(group_cs_core)
        db.session.add(group_se_elective)
        db.session.commit()  # Commit the courses to the database so their IDs are generated

        # Create group elements
        group_element_1 = GroupElement(research_flag=True, capstone_flag=False, group_id=group_cs_core.id, unit_id=unit_data_structures.id)
        group_element_2 = GroupElement(research_flag=False, capstone_flag=True, group_id=group_cs_core.id, unit_id=unit_algorithms.id)
        group_element_3 = GroupElement(research_flag=False, capstone_flag=True, group_id=group_se_elective.id, unit_id=unit_testing.id)
        db.session.add(group_element_1)
        db.session.add(group_element_2)
        db.session.add(group_element_3)

        db.session.commit()  # Commit the changes
