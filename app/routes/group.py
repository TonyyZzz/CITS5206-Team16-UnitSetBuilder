from flask import request, redirect, url_for, flash, jsonify
from . import group
from ..models import Group, UnitSet, Specialisation
from .. import db

@group.route('/add_group_to_unitset', methods = ['POST'])
def addGroupToUnitSet():
    # Get JSON data from request
    data = request.get_json()
    unit_set_id = data.get('unit_set_id')
    group_type = data.get('group_type')

    if not unit_set_id or not group_type:
        return jsonify({'success': False, 'error': 'Invalid data provided'}), 400

    # Fetch the UnitSet object
    unit_set = UnitSet.query.get(unit_set_id)
    if not unit_set:
        return jsonify({'success': False, 'error': 'Unit set not found'}), 404

    # Create a new Group and associate it with the UnitSet
    new_group = Group(group_type=group_type, unit_set_id=unit_set_id)
    db.session.add(new_group)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Group added to unit set successfully','group_id': new_group.id})


@group.route('/add_group_to_specialization', methods=['POST'])
def addGroupToSpecialization():
    # Get JSON data from request
    data = request.get_json()
    specialization_id = data.get('specialization_id')
    group_type = data.get('group_type')

    if not specialization_id or not group_type:
        return jsonify({'success': False, 'error': 'Invalid data provided'}), 400

    # Fetch the Specialisation object
    specialization = Specialisation.query.get(specialization_id)
    if not specialization:
        return jsonify({'success': False, 'error': 'Specialisation not found'}), 404

    # Create a new Group and associate it with the Specialisation
    new_group = Group(group_type=group_type, specialisation_id=specialization_id)
    db.session.add(new_group)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Group added to specialization successfully', 'group_id': new_group.id})


@group.route('/delete_group/<int:group_id>', methods=['DELETE'])
def deleteGroup(group_id):
    # Find the group by id
    group = Group.query.get(group_id)
    
    # If the group doesn't exist, return an error
    if not group:
        return jsonify({'success': False, 'error': 'Group not found'}), 404

    # Delete the group
    db.session.delete(group)
    db.session.commit()

    # Return a success response
    return jsonify({'success': True, 'message': 'Group deleted successfully'})