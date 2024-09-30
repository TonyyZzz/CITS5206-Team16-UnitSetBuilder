from app import create_app, db
from app.models import Specialisation


# Create a test function to fill in the Specialisation table with test data
def populate_specialisations():
    # Sample test data
    specialisations = [
        {
            'name': 'Computer Science',
            'code': 'CS101',
            'description': 'A specialisation in Computer Science.',
            'outcome': 'Graduate with strong programming skills.',
            'note': 'Includes core subjects in programming and algorithms.'
        },
        {
            'name': 'Data Science',
            'code': 'DS201',
            'description': 'A specialisation in Data Science.',
            'outcome': 'Graduate with skills in data analysis and machine learning.',
            'note': 'Includes subjects in statistics and data modeling.'
        },
        {
            'name': 'Artificial Intelligence',
            'code': 'AI301',
            'description': 'A specialisation in Artificial Intelligence.',
            'outcome': 'Graduate with skills in AI and machine learning techniques.',
            'note': 'Focuses on deep learning and neural networks.'
        }
    ]

    # Add each specialisation to the database
    for spec_data in specialisations:
        specialisation = Specialisation(
            name=spec_data['name'],
            code=spec_data['code'],
            description=spec_data['description'],
            outcome=spec_data['outcome'],
            note=spec_data['note']
        )
        db.session.add(specialisation)

    # Commit the changes to the database
    db.session.commit()
    print(f"{len(specialisations)} specialisations added successfully.")


if __name__ == '__main__':
    # Initialize the Flask app and the database with the appropriate config
    app = create_app('development')  # or 'testing', 'production', etc.
    with app.app_context():
        # Optionally drop all tables and recreate them for testing purposes
        # db.drop_all()
        # db.create_all()

        # Populate the Specialisation table
        populate_specialisations()

