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

    return jsonify({'success': True, 'message': 'Group added to unit set successfully'})


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

    return jsonify({'success': True, 'message': 'Group added to specialization successfully'})


@group.route('/deleteGroup/<int:group_id>', methods=['POST'])
def deleteGroup(group_id):
    # Retrieve the group by its ID
    group = Group.query.get(group_id)
    
    # Check if the group exists
    if not group:
        flash(f'Group with ID {group_id} does not exist', 'error')
        return redirect(url_for('main.unit_set'))  # Redirect to the group list or an error page

    try:
        # Delete the group
        db.session.delete(group)
        db.session.commit()

        flash('Group deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash(f'Error deleting group: {str(e)}', 'error')

    # Redirect to a page showing groups or home page
    return redirect(url_for('group.view_groups'))