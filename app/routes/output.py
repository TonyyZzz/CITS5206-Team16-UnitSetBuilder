from flask import Flask, render_template, send_file, Blueprint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from ..models import Course, UnitSet, Specialisation

output = Blueprint('output', __name__)

def generate_course_pdf(course_id):
    # Step 1: Retrieve detailed course information
    course_details = get_course_details(course_id)
    if not course_details:
        return "Course not found", 404

    # Step 2: Create a PDF buffer
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)

    # Step 3: Add course information to the PDF
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(50, 800, f"{course_details['title']}")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(50, 780, f"Course Code: {course_details['code']}")
    pdf.drawString(50, 760, f"Description: {course_details['description'] or 'N/A'}")

    y_position = 720

    # Step 4: Add Unit Sets, Groups, and Elements to the PDF
    pdf.setFont("Times-Bold", 16)
    pdf.drawString(50, y_position, "Unit Sets:")
    y_position -= 20
    pdf.setFont("Times-Roman", 14)

    for unit_set in course_details['unit_sets']:
        pdf.drawString(50, y_position, f"{unit_set['title']}")
        y_position -= 20
        

        for group in unit_set['groups']:
            pdf.setFont("Times-Bold", 14)
            
            group_type = group['group_type'].lower()

            # Set different background colors based on group_type
            if group_type == 'core':
                bg_color = (204/255, 207/255, 234/255)  # RGB for core background
            elif group_type == 'option':
                bg_color = (251/255, 244/255, 207/255)  # RGB for option background
            elif group_type == 'customised':
                bg_color = (206/255, 232/255, 253/255)  # RGB for customised background
            elif group_type == 'conversion':
                bg_color = (237/255, 213/255, 220/255)  # RGB for conversion background
            else:
                bg_color = (1, 1, 1)  # Default white background if no match
            
            # Draw a background rectangle (adjust size based on text length and position)
            pdf.setFillColorRGB(*bg_color)
            pdf.rect(50, y_position - 5, 490, 20, fill=1)  # Adjust rectangle width and height as needed
            
            # Set text color to black or any contrasting color
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(60, y_position, f"{group['group_type']} - {group['note']}")
            
            y_position -= 20



            for element in group['group_elements']:
                pdf.setFont("Times-Roman", 12)
                pdf.setFillColorRGB(0, 0, 0)
                pdf.drawString(80, y_position, f"• {element['unit_details']['name']} : {element['unit_details']['credit_point']}")
                y_position -= 20
                if y_position < 50:  # Check if the y_position is too low for the content
                    pdf.showPage()  # Add a new page
                    y_position = 800

    # Step 5: Add Specialisation information (if any)
    if course_details.get('specialisations'):
        y_position -= 20
        pdf.setFont("Times-Bold", 16)
        pdf.drawString(50, y_position, "Specialisations:")
        y_position -= 20
        pdf.setFont("Times-Roman", 14)

        for specialisation in course_details['specialisations']:
            pdf.drawString(50, y_position, f"{specialisation['name']}")
            y_position -= 20

            for group in specialisation['groups']:
                pdf.setFont("Times-Bold", 14)
                pdf.drawString(70, y_position, f"{group['group_type']} - {group['note']}")
                group_type = group['group_type'].lower()

                # Set different background colors based on group_type
                if group_type == 'core':
                    bg_color = (204/255, 207/255, 234/255)  # RGB for core background
                elif group_type == 'option':
                    bg_color = (251/255, 244/255, 207/255)  # RGB for option background
                elif group_type == 'customised':
                    bg_color = (206/255, 232/255, 253/255)  # RGB for customised background
                elif group_type == 'conversion':
                    bg_color = (237/255, 213/255, 220/255)  # RGB for conversion background
                else:
                    bg_color = (1, 1, 1)  # Default white background if no match
                
                # Draw a background rectangle (adjust size based on text length and position)
                pdf.setFillColorRGB(*bg_color)
                pdf.rect(50, y_position - 5, 490, 20, fill=1)  # Adjust rectangle width and height as needed
                
                # Set text color to black or any contrasting color
                pdf.setFillColorRGB(0, 0, 0)
                pdf.drawString(60, y_position, f"{group['group_type']} - {group['note']}")

                
                y_position -= 20

                for element in group['group_elements']:
                    pdf.setFont("Times-Roman", 12)
                    pdf.setFillColorRGB(0, 0, 0)
                    pdf.drawString(80, y_position, f"• {element['unit_details']['name']} : {element['unit_details']['credit_point']}")
                    y_position -= 20
                    if y_position < 50:
                        pdf.showPage()
                        y_position = 800

    # Step 6: Finalize and Save PDF
    pdf.showPage()
    pdf.save()
    pdf_buffer.seek(0)

    return pdf_buffer

@output.route('/download-course-pdf/<int:course_id>', methods=['GET'])
def download_course_pdf(course_id):
    # Generate the PDF for the given course_id
    try:
        pdf_buffer = generate_course_pdf(course_id)
    except ValueError as e:
        return str(e), 404

    # Send the PDF as a downloadable file
    return send_file(pdf_buffer, as_attachment=False, download_name=f"course_{course_id}_summary.pdf", mimetype='application/pdf')

def get_course_details(course_id):
    # Retrieve the course details using SQLAlchemy ORM
    course = Course.query.filter_by(id=course_id).first()
    
    if not course:
        return None  # Return None if the course is not found
    
    # Gather the main course information
    course_data = course.to_dict()  # Convert course object to dictionary using your custom to_dict method
    
    # Retrieve related Unit Sets and their Groups and Group Elements
    unit_sets = []
    for unit_set in course.unit_sets:
        unit_set_data = unit_set.to_dict()
        
        # Retrieve Groups related to the Unit Set
        groups = []
        for group in unit_set.groups:
            group_data = group.to_dict()

            # Retrieve Group Elements related to the Group
            group_elements = []
            for element in group.group_elements:
                element_data = element.to_dict()
                
                # Retrieve the associated Unit details from the Group Element
                unit_data = element.unit.to_dict()
                element_data['unit_details'] = unit_data  # Add unit details to the element
                
                group_elements.append(element_data)
            
            group_data['group_elements'] = group_elements  # Attach all group elements to the group
            groups.append(group_data)
        
        unit_set_data['groups'] = groups  # Attach all groups to the unit set
        unit_sets.append(unit_set_data)

    # Attach all unit sets to the course data
    course_data['unit_sets'] = unit_sets

    # Retrieve related Specialisations and their Groups
    specialisations = []
    for course_specialisation in course.course_specialisations:
        specialisation = course_specialisation.specialisation
        if specialisation:
            specialisation_data = specialisation.to_dict()

            # Retrieve Groups related to the Specialisation
            specialisation_groups = []
            for group in specialisation.groups:
                group_data = group.to_dict()

                # Retrieve Group Elements related to the Group
                group_elements = []
                for element in group.group_elements:
                    element_data = element.to_dict()

                    # Retrieve the associated Unit details from the Group Element
                    unit_data = element.unit.to_dict()
                    element_data['unit_details'] = unit_data

                    group_elements.append(element_data)

                group_data['group_elements'] = group_elements  # Attach all group elements to the group
                specialisation_groups.append(group_data)
            
            specialisation_data['groups'] = specialisation_groups  # Attach all groups to the specialisation
            specialisations.append(specialisation_data)
    
    # Attach all specialisations to the course data
    course_data['specialisations'] = specialisations

    return course_data  # Return the detailed course data


