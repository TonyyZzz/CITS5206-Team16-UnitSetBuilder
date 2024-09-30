# test_base.py
import unittest
from app import create_app, db  # Replace 'app' with the name of your Flask app package
from app.models import User, Course, UnitSet, Specialisation, Group, GroupElement, Unit, CourseSpecialisation

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Executed once before any test methods in the class."""
        # Create the Flask app and set up the testing configuration
        cls.app = create_app(config_name='TESTING')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Executed once after all test methods in the class."""
        cls.app_context.pop()

    def setUp(self):
        """Executed before each test method."""
        # Set up the database and insert mock data
        db.create_all()
        self.insert_mock_data()

    def tearDown(self):
        """Executed after each test method."""
        # Remove the database session and drop all tables
        db.session.remove()
        db.drop_all()

    def insert_mock_data(self):
        """Insert mock data for testing purposes."""
        # Create sample users
        user1 = User(username='testuser1', email='testuser1@example.com', password_hash='hashedpassword')
        user2 = User(username='testuser2', email='testuser2@example.com', password_hash='hashedpassword')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Create courses
        course1 = Course(title='Computer Science', code='CS101', description='Intro to Computer Science')
        course2 = Course(title='Software Engineering', code='SE101', description='Software Engineering Basics')
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()

        # Create unit sets
        unit_set1 = UnitSet(title='Core Units for CS', description='Core units for Computer Science', note='Core', course_id=course1.id)
        unit_set2 = UnitSet(title='Core Units for SE', description='Core units for Software Engineering', note='Core', course_id=course2.id)
        db.session.add(unit_set1)
        db.session.add(unit_set2)
        db.session.commit()

        # Create specialisations
        specialisation1 = Specialisation(name='AI Specialisation', code='AI101', description='AI related courses', note='AI focus')
        specialisation2 = Specialisation(name='Software Development', code='SD101', description='Software Development related courses', note='SD focus')
        db.session.add(specialisation1)
        db.session.add(specialisation2)
        db.session.commit()

        # Create groups
        group1 = Group(group_type='Core Group', note='All core units for CS', unit_set_id=unit_set1.id)
        group2 = Group(group_type='Elective Group', note='Elective units for SE', unit_set_id=unit_set2.id)
        db.session.add(group1)
        db.session.add(group2)
        db.session.commit()

        # Create units
        unit1 = Unit(name='Data Structures', code='CS102', description='Data Structures in CS')
        unit2 = Unit(name='Algorithms', code='CS103', description='Algorithms in CS')
        unit3 = Unit(name='Software Testing', code='SE102', description='Software Testing in SE')
        db.session.add(unit1)
        db.session.add(unit2)
        db.session.add(unit3)
        db.session.commit()

        # Create group elements
        group_element1 = GroupElement(research_flag=True, capstone_flag=False, group_id=group1.id, unit_id=unit1.id)
        group_element2 = GroupElement(research_flag=False, capstone_flag=True, group_id=group1.id, unit_id=unit2.id)
        group_element3 = GroupElement(research_flag=False, capstone_flag=True, group_id=group2.id, unit_id=unit3.id)
        db.session.add(group_element1)
        db.session.add(group_element2)
        db.session.add(group_element3)
        db.session.commit()
