from app import create_app, db
from app.models import User, Unit, Group, UnitSet, Specialisation, Course

def populate_dummy_data():
    # Create an application context
    app = create_app('development')  # Adjust configuration name if necessary

    # Use app context for database operations
    with app.app_context():
        # Check if the database is already populated to avoid duplication
        if Unit.query.first():
            print("Database already has data. Skipping population.")
            return

        # Create some dummy users
        user1 = User(username='john_doe', email='john@example.com', password_hash='hashed_password1')
        user2 = User(username='jane_smith', email='jane@example.com', password_hash='hashed_password2')

        # Add users to the session
        db.session.add_all([user1, user2])

        # Create dummy units
        unit1 = Unit(name='Mathematics 101', code='MATH101', description='Introduction to basic mathematics.')
        unit2 = Unit(name='Physics 202', code='PHYS202', description='Intermediate physics concepts.')
        unit3 = Unit(name='Introduction to Chemistry', code='CHEM101', description='Basics of chemistry.')
        unit4 = Unit(name='Biology Basics', code='BIO101', description='Fundamentals of biology.')
        unit5 = Unit(name='Advanced Calculus', code='CALC301', description='Advanced topics in calculus.')

        # Add units to the session
        db.session.add_all([unit1, unit2, unit3, unit4, unit5])

        # Create dummy courses
        course1 = Course(title='Bachelor of Science')
        course2 = Course(title='Bachelor of Engineering')

        db.session.add_all([course1, course2])

        # Create dummy specialisations
        spec1 = Specialisation(name='Mathematics Major', code='MATH', description='Specialization in Mathematics')
        spec2 = Specialisation(name='Physics Major', code='PHYS', description='Specialization in Physics')

        db.session.add_all([spec1, spec2])

        # Create dummy unit sets
        unit_set1 = UnitSet(title='Core Mathematics Units', description='Core units for mathematics major',
                            note='Important', course=course1)
        unit_set2 = UnitSet(title='Core Physics Units', description='Core units for physics major', note='Essential',
                            course=course2)

        db.session.add_all([unit_set1, unit_set2])

        # Create dummy groups linked to UnitSet
        group1 = Group(group_type='Core', note='Group 1 Note', rule_type='All', custom_title_text='Core Group',
                       value='1', custom_value='Custom 1', unit_set_id=unit_set1.id)
        group2 = Group(group_type='Elective', note='Group 2 Note', rule_type='Any', custom_title_text='Elective Group',
                       value='2', custom_value='Custom 2', unit_set_id=unit_set2.id)

        db.session.add_all([group1, group2])

        # Commit the session to save the data to the database
        db.session.commit()

        print("Dummy data successfully populated in the database.")

if __name__ == '__main__':
    populate_dummy_data()
