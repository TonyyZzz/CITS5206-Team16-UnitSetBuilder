const units = [
    { id: '00', code: '10000', title: 'Master of Information Technology (coursework)', status: false, editable: true },
    { id: '01', code: '10001', title: 'Master of Information Technology (AI Stream)', status: false, editable: false },
    // You can add more units as needed
];

function showSuggestions() {
    const input = document.getElementById('search-input').value.toLowerCase();
    const suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = '';  // Clear previous suggestions

    // If input is empty, hide the suggestions list and return
    if (input.trim() === '') {
        suggestions.style.display = 'none'; // Hide suggestions
        return;
    }

    suggestions.style.display = 'block'; // Show suggestions if input is not empty

    units.forEach(unit => {
        if (unit.title.toLowerCase().includes(input)) {
            const suggestionItem = document.createElement('a');
            suggestionItem.href = "#";
            suggestionItem.classList.add('list-group-item', 'list-group-item-action');
            suggestionItem.innerHTML = `
                ${unit.title} <span class="badge bg-success rounded-pill" onclick="addToTable('${unit.id}')">+</span>
            `;
            suggestions.appendChild(suggestionItem);
        }
    });
}

function addToTable(unitId) {
    const unit = units.find(u => u.id === unitId);
    const tableBody = document.getElementById('unit-table');
    const row = document.createElement('tr');
    
    row.innerHTML = `
        <td>
            ${unit.editable 
                ? '<button class="btn btn-outline-secondary btn-sm status-button">✎</button>' 
                : '<span class="text-danger">×</span>'
            }
        </td>
        <td>${unit.id}</td>
        <td>${unit.code}</td>
        <td>${unit.title}</td>
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
