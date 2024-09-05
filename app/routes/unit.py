from flask import request, redirect, url_for, flash, render_template
from . import unit
from ..models import Group, GroupElement, Unit
from .. import db

@unit.route('/addUnit', methods=['POST'])
def addUnit():
    try:
        # Get data from the form
        group_id = request.form.get('group_id')
        unit_id = request.form.get('unit_id')

        # Validate if the group and unit exist
        group = Group.query.get(group_id)
        if not group:
            flash(f'Group with ID {group_id} does not exist', 'error')
            return redirect(url_for('main.unit_set'))

        unit = Unit.query.get(unit_id)
        if not unit:
            flash(f'Unit with ID {unit_id} does not exist', 'error')
            return redirect(url_for('main.unit_set'))

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

        flash('GroupElement added successfully!', 'success')
        return redirect(url_for('main.unit_set'))

    except Exception as e:
        flash(f'Error adding GroupElement: {str(e)}', 'error')
        return redirect(url_for('groupelements.add_group_element_form'))
    
@unit.route('/editUnit/<int:element_id>', methods=['POST'])
def editUnit(element_id):
    try:
        # Retrieve the existing GroupElement by ID
        group_element = GroupElement.query.get(element_id)
        if not group_element:
            flash(f'GroupElement with ID {element_id} does not exist', 'error')
            return redirect(url_for('main.unit_set'))

        # Get updated data from the form
        research_flag = bool(request.form.get('research_flag', False))
        capstone_flag = bool(request.form.get('capstone_flag', False))

        # Update the GroupElement fields
        group_element.research_flag = research_flag
        group_element.capstone_flag = capstone_flag

        # Save changes to the database
        db.session.commit()

        flash('GroupElement updated successfully!', 'success')
        return redirect(url_for('groupelements.view_group_elements'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error editing GroupElement: {str(e)}', 'error')
        return redirect(url_for('main.unit_set'))
    
@unit.route('/deleteUnit/<int:element_id>', methods=['POST'])
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

