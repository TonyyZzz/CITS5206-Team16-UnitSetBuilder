from flask_bcrypt import Bcrypt
from app import create_app, db
from app.models import User, Unit, Group, UnitSet, Specialisation, Course, GroupElement

bcrypt = Bcrypt()

def populate_dummy_data():
    # Create an application context
    app = create_app('development')  # Adjust configuration name if necessary

    # Use app context for database operations
    with app.app_context():
        # Check if the database is already populated to avoid duplication
        if Unit.query.first() or Course.query.first():
            print("Database already has data. Skipping population.")
            return

        # Create some dummy users with hashed passwords using Flask-Bcrypt
        user1 = User(username='test', email='test@test.com', password_hash=bcrypt.generate_password_hash('test').decode('utf-8'))

        # Add users to the session
        db.session.add_all([user1])

        # Create dummy units with credit_points included
        unit1 = Unit(name='Mathematics 101', code='MATH101', description='Introduction to basic mathematics.',
                     credit_points=6)
        unit2 = Unit(name='Physics 202', code='PHYS202', description='Intermediate physics concepts.', credit_points=6)
        unit3 = Unit(name='Introduction to Chemistry', code='CHEM101', description='Basics of chemistry.',
                     credit_points=6)
        unit4 = Unit(name='Biology Basics', code='BIO101', description='Fundamentals of biology.', credit_points=6)
        unit5 = Unit(name='Advanced Calculus', code='CALC301', description='Advanced topics in calculus.',
                     credit_points=6)

        # Add units to the session
        db.session.add_all([unit1, unit2, unit3, unit4, unit5])

        # Create dummy courses
        course1 = Course(title='Bachelor of Science', code='BS01',
                         description='A program focused on science disciplines.')
        course2 = Course(title='Bachelor of Engineering', code='BE01',
                         description='A program focused on engineering disciplines.')
        course3 = Course(title='Master of Information Technology', code='MIT01', description='Advanced studies in IT.')
        course4 = Course(title='Master of Business Administration', code='MBA01',
                         description='Advanced studies in business administration.')
        course5 = Course(title='Doctor of Philosophy in Physics', code='PhDPhys01',
                         description='Research-focused program in physics.')

        db.session.add_all([course1, course2, course3, course4, course5])

        # Create dummy specialisations
        spec1 = Specialisation(name='Mathematics Major', code='MATH', description='Specialization in Mathematics')
        spec2 = Specialisation(name='Physics Major', code='PHYS', description='Specialization in Physics')

        db.session.add_all([spec1, spec2])

        # Create dummy unit sets, link to courses
        unit_set1 = UnitSet(title='Core Mathematics Units', description='Core units for mathematics major',
                            note='Important', course=course1)
        unit_set2 = UnitSet(title='Core Physics Units', description='Core units for physics major', note='Essential',
                            course=course2)

        db.session.add_all([unit_set1, unit_set2])
        db.session.commit()  # Commit to get the IDs generated

        # Create dummy groups linked to UnitSet and Specialisation
        group1 = Group(group_type='Core', note='Group 1 Note', rule_type='All', custom_title_text='Core Group',
                       value='1', custom_value='Custom 1', unit_set_id=unit_set1.id)
        group2 = Group(group_type='Elective', note='Group 2 Note', rule_type='Any', custom_title_text='Elective Group',
                       value='2', custom_value='Custom 2', unit_set_id=unit_set2.id)
        group3 = Group(group_type='Specialisation', note='Specialisation Group Note', rule_type='Any',
                       custom_title_text='Physics Specialisation', value='3', custom_value='Custom 3',
                       specialisation_id=spec2.id)

        db.session.add_all([group1, group2, group3])
        db.session.commit()  # Commit again to ensure the groups get their IDs

        # Now create GroupElements linked to groups
        group_element1 = GroupElement(group_id=group1.id, unit_id=unit1.id)
        group_element2 = GroupElement(group_id=group1.id, unit_id=unit5.id)
        group_element3 = GroupElement(group_id=group2.id, unit_id=unit2.id)
        group_element4 = GroupElement(group_id=group3.id, unit_id=unit3.id)

        db.session.add_all([group_element1, group_element2, group_element3, group_element4])

        # Commit the session to save the data to the database
        db.session.commit()

        print("Dummy data successfully populated in the database.")


if __name__ == '__main__':
    bcrypt.init_app(create_app('development'))  # Initialize Flask-Bcrypt
    populate_dummy_data()
