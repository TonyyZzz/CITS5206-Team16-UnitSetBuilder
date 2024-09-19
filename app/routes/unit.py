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

        return jsonify({"success": True})  # Send success response

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    
@unit.route('/deleteUnit/<int:element_id>', methods=['DELETE'])
def deleteUnit(element_id):
    try:
        # Retrieve the GroupElement by ID
        group_element = GroupElement.query.get(element_id)
        if not group_element:
            flash(f'GroupElement with ID {element_id} does not exist', 'error')
            return redirect(url_for('groupelements.view_group_elements'))

        # Delete the GroupElement
        db.session.delete(group_element)
        db.session.commit()

        flash('GroupElement deleted successfully!', 'success')
        return redirect(url_for('main.unit_set'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting GroupElement: {str(e)}', 'error')
        return redirect(url_for('main.unit_set'))

