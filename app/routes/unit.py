from flask import request, redirect, url_for, flash, jsonify, Blueprint
from . import unit
from ..models import Group, GroupElement, Unit
from .. import db

unit = Blueprint('unit', __name__)

@unit.route('/addUnit', methods=['POST'])
def addUnit():
    try:
        # Get data from the JSON request
        data = request.get_json()
        group_id = data.get('group_id')
        unit_id = data.get('unit_id')

        # Validate if the group and unit exist
        group = Group.query.get(group_id)
        if not group:
            return jsonify({"success": False, "error": f"Group with ID {group_id} does not exist"})


        unit = Unit.query.get(unit_id)
        if not unit:
            return jsonify({"success": False, "error": f"Unit with ID {unit_id} does not exist"})


        # Create a new GroupElement
        new_group_element = GroupElement(
            group_id=group_id,
            unit_id=unit_id,
            research_flag=False,
            capstone_flag=False
        )

        # Add the GroupElement to the database
        db.session.add(new_group_element)
        db.session.commit()

        return jsonify({"success": True, 'element_id': new_group_element.id})  # Send success response

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    
@unit.route('/delete_unit', methods=['DELETE'])
def delete_unit():
    # Get the unit ID from the request body (JSON)
    data = request.get_json()
    unit_id = data.get('unit_id')

    if not unit_id:
        return jsonify({'success': False, 'error': 'No unit ID provided'}), 400

    # Find the GroupElement or Unit by its ID and delete it
    unit = GroupElement.query.filter_by(id=unit_id).first()

    if not unit:
        return jsonify({'success': False, 'error': 'Unit not found'}), 404

    # Delete the unit from the database
    db.session.delete(unit)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Unit deleted successfully'})


@unit.route('/calculate_points/<int:group_id>', methods=['GET'])
def calculate_points(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'success': False, 'error': 'Group not found'}), 404

    # Calculate the total points by summing the credit points of all units in this group
    total_points = sum([element.unit.credit_points for element in group.group_elements])

    return jsonify({'success': True, 'total_points': total_points})
