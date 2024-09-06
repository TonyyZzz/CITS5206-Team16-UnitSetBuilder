from flask import request, redirect, url_for, flash, render_template
from . import group
from ..models import Group, UnitSet
from .. import db

@group.route('/addGroup', methods = ['POST'])
def addGroup():

# Get the unit_set_id from the request (e.g., from a form or JSON data)
    unit_set_id = request.form.get('unit_set_id')
    group_type = request.form.get('group_type')
    note = request.form.get('note')
    rule_type = request.form.get('rule_type')
    custom_title_text = request.form.get('custom_title_text')
    value = request.form.get('value')
    custom_value = request.form.get('custom_value')
    is_specialisation = bool(request.form.get('is_specialisation', False))  # Default to False

    # Validate that the UnitSet exists
    unit_set = UnitSet.query.get(unit_set_id)
    if not unit_set:
        flash(f'UnitSet with ID {unit_set_id} does not exist', 'error')
        return redirect(url_for('main.unit_set'))  # Redirect to a form page or handle the error accordingly

    # Create a new Group object
    new_group = Group(
        group_type=group_type,
        note=note,
        rule_type=rule_type,
        custom_title_text=custom_title_text,
        value=value,
        custom_value=custom_value,
        is_specialisation=is_specialisation,
        unit_set_id=unit_set.id  # Associate the group with the given UnitSet
    )

    # Add the new group to the database
    db.session.add(new_group)
    db.session.commit()

    # Flash a success message and redirect to a relevant page
    flash('Group added successfully to UnitSet!', 'success')
    return redirect(url_for('main.unitset', unit_set_id=unit_set.id))  # Redirect to a page showing groups for the UnitSet

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

@group.route('/editGroup/<int:group_id>', methods=['POST'])
def edit_group(group_id):
    # Retrieve the group by ID
    group = Group.query.get(group_id)

    # Check if the group exists
    if not group:
        flash(f'Group with ID {group_id} does not exist', 'error')
        return redirect(url_for('group.view_groups'))  # Redirect to the list of groups

    # If it's a POST request, handle the form submission
    if request.method == 'POST':
        # Get updated data from the form
        note = request.form.get('note')
        rule_type = request.form.get('rule_type')
        custom_title_text = request.form.get('custom_title_text')
        value = request.form.get('value')
        custom_value = request.form.get('custom_value')

        # Update the group fields with the new data
        group.note = note
        group.rule_type = rule_type
        group.custom_title_text = custom_title_text
        group.value = value
        group.custom_value = custom_value

        # Save the changes to the database
        try:
            db.session.commit()
            flash('Group updated successfully!', 'success')
            return redirect(url_for('group.view_groups'))  # Redirect to the group listing or relevant page
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            flash(f'Error updating group: {str(e)}', 'error')

    # If it's a GET request, render the edit form with the existing data
    return render_template('edit_group.html', group=group)