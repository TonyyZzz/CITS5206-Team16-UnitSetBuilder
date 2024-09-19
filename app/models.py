from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit_sets = db.relationship('UnitSet', backref='course', lazy=True)
    course_specialisations = db.relationship('CourseSpecialisation', backref='course', lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'description': self.description
        }

class UnitSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    note = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    # Establish the relationship to Group with a foreign key
    groups = db.relationship('Group', backref='unit_set', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'note': self.note,
            'groups': [group.to_dict() for group in self.groups]

        }

class Specialisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    outcome = db.Column(db.Text)
    note = db.Column(db.Text)
    groups = db.relationship('Group', backref='specialisation', lazy=True)
    course_specialisations = db.relationship('CourseSpecialisation', backref='specialisation', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'note': self.note,
            'groups': [group.to_dict() for group in self.groups]

        }


class CourseSpecialisation(db.Model):
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    specialisation_id = db.Column(db.Integer, db.ForeignKey('specialisation.id'), primary_key=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_type = db.Column(db.String(50))
    note = db.Column(db.Text)
    rule_type = db.Column(db.String(50))
    custom_title_text = db.Column(db.String(255))
    value = db.Column(db.String(255))
    custom_value = db.Column(db.String(255))
    is_specialisation = db.Column(db.Boolean, default=False)

    # Correct foreign key to UnitSet
    unit_set_id = db.Column(db.Integer, db.ForeignKey('unit_set.id'), nullable=True)

    # Correct foreign key to Specialisation
    specialisation_id = db.Column(db.Integer, db.ForeignKey('specialisation.id'), nullable=True)

    parent_group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)

    # Self-referential relationship for parent-child groups
    children = db.relationship('Group', backref=db.backref('parent', remote_side=[id]), lazy=True)

    group_elements = db.relationship('GroupElement', backref='group', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'group_type': self.group_type,
            'note': self.note,
            'is_specialisation': self.is_specialisation,
            'unit_set_id' : self.unit_set_id ,
            'specialisation_id' : self.specialisation_id ,
            'elements': [element.to_dict() for element in self.group_elements]  # Include related groups

        }


class GroupElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    research_flag = db.Column(db.Boolean, default=False)
    capstone_flag = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    unit = db.relationship('Unit', backref='group_elements')

    def to_dict(self):
        return {
            'id': self.id,
            'research_flag': self.research_flag,
            'capstone_flag': self.capstone_flag,
            'unit_id': self.unit_id,
            'unit_name': self.unit.name  # Access the unit's name via the relationship
        }

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # New field added
    # Additional fields for Unit model should go here
    # New fields
    code = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
