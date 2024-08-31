from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_sets = db.relationship('UnitSet', backref='course', lazy=True)
    course_specialisations = db.relationship('CourseSpecialisation', backref='course', lazy=True)

class UnitSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    note = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    groups = db.relationship('Group', backref='unit_set', lazy=True)

class Specialisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    outcome = db.Column(db.Text)
    note = db.Column(db.Text)
    groups = db.relationship('Group', backref='specialisation', lazy=True)
    course_specialisations = db.relationship('CourseSpecialisation', backref='specialisation', lazy=True)

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
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    specialisation_id = db.Column(db.Integer, db.ForeignKey('specialisation.id'), nullable=True)
    parent_group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    children = db.relationship('Group', backref=db.backref('parent', remote_side=[id]), lazy=True)
    group_elements = db.relationship('GroupElement', backref='group', lazy=True)

class GroupElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    research_flag = db.Column(db.Boolean, default=False)
    capstone_flag = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Additional fields for Unit model should go here