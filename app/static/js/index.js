let selectedCourse = null;

function showSuggestions() {
    const input = document.getElementById('search-input').value.toLowerCase();
    const suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = '';  // Clear previous suggestions

    // If input is empty, hide the suggestions list and return
    if (input.trim() === '') {
        suggestions.style.display = 'none'; // Hide suggestions
        return;
    }

    // Fetch suggestions from the server
    fetch(`/search_courses?query=${encodeURIComponent(input)}`)
        .then(response => response.json())
        .then(courses => {
            suggestions.style.display = 'block'; // Show suggestions if input is not empty

            courses.forEach(course => {
                const suggestionItem = document.createElement('a');
                suggestionItem.href = "#";
                suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                suggestionItem.innerHTML = `
                    ${course.title} <span class="badge bg-success rounded-pill" onclick="selectCourse('${course.id}', '${course.code}', '${course.title}')">+</span>
                `;
                suggestions.appendChild(suggestionItem);
            });
        })
        .catch(error => console.error('Error fetching search results:', error));
}

function selectCourse(courseId, courseCode, courseTitle) {
    selectedCourse = { id: courseId, code: courseCode, title: courseTitle };
    console.log('Selected course:', selectedCourse);  // For debugging
    addToTable(courseId, courseCode, courseTitle);  // Automatically add selected course to the table
}

function addToTable(courseId, courseCode, courseTitle) {
    const tableBody = document.getElementById('unit-table');
    const row = document.createElement('tr');

    row.innerHTML = `
        <td>
            <button class="btn btn-outline-secondary btn-sm status-button">✎</button>
        </td>
        <td>${courseId}</td>
        <td>${courseCode}</td>
        <td>${courseTitle}</td>
        <td>
            <span class="checkbox-unchecked status-button" onclick="toggleCheckbox(this)"></span>
            <button class="btn btn-danger btn-sm status-button" onclick="removeFromTable(this)"><img src="https://cdn-icons-png.flaticon.com/512/3096/3096673.png" alt="Delete"></button>
        </td>
    `;

    tableBody.appendChild(row);
}

function toggleCheckbox(element) {
    if (element.classList.contains('checkbox-unchecked')) {
        element.classList.remove('checkbox-unchecked');
        element.innerHTML = '✓';
        element.style.backgroundColor = '#0d6efd';
        element.style.color = 'white';
    } else {
        element.classList.add('checkbox-unchecked');
        element.innerHTML = '';
        element.style.backgroundColor = 'white';
        element.style.color = 'black';
    }
}

function removeFromTable(button) {
    const row = button.closest('tr');
    row.remove();
}

function createUnitSetBuilder() {
    if (selectedCourse) {
        // Set the action URL with the course ID
        window.location.href = `/grouping-page?courseId=${selectedCourse.id}`;
    } else {
        alert('Please select a course first.');
    }
}


document.getElementById('search-input').addEventListener('input', showSuggestions);
