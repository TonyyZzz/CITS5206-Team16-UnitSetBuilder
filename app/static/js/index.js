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
                    ${course.title} <span class="badge bg-success rounded-pill" onclick="addToTable('${course.id}', '${course.code}', '${course.title}')">+</span>
                `;
                suggestions.appendChild(suggestionItem);
            });
        })
        .catch(error => console.error('Error fetching search results:', error));
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
    const checkboxes = document.querySelectorAll('.status-button');
    const hasCheckedCourse = Array.from(checkboxes).some(box => box.innerHTML === '✓');

    if (hasCheckedCourse) {
        window.location.href = '{{ url_for("main.unit_set") }}';
    } else {
        alert('Please select at least one course.');
    }
}

document.getElementById('search-input').addEventListener('input', showSuggestions);
