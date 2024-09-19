document.addEventListener('DOMContentLoaded', () => {
    // Get references to elements
    const openPopupBtn = document.getElementById('specialization-button');
    const closePopupBtn = document.getElementById('closePopupBtn');
    const popup = document.getElementById('popup');
    const optionSelect = document.getElementById('optionSelect');
    const existingOptionSection = document.getElementById('existingOptionSection');
    const newOptionSection = document.getElementById('newOptionSection');
    const detailsForm = document.getElementById('detailsForm');
    const detailsDisplay = document.getElementById('detailsDisplay');

    // Open the popup
    openPopupBtn.addEventListener('click', () => {
        popup.style.display = 'block';
    });

    // Close the popup
    closePopupBtn.addEventListener('click', () => {
        popup.style.display = 'none';
    });

    optionSelect.addEventListener('change', () => {
        switch (optionSelect.value) {
            case 'add':
                existingOptionSection.style.display = 'none';
                newOptionSection.style.display = 'block';
                break;
            case 'select':
                existingOptionSection.style.display = 'block';
                newOptionSection.style.display = 'none';
                break;
            case 'default':
                existingOptionSection.style.display = 'none';
                newOptionSection.style.display = 'none';
                break;
        }
    });

    // Function to show suggestions for group search
    function showGroupSuggestions() {
        const input = document.getElementById('existingOption').value.toLowerCase();
        const suggestions = document.getElementById('group-suggestions');
        suggestions.innerHTML = '';  // Clear previous suggestions

        // If input is empty, hide the suggestions list and return
        if (input.trim() === '') {
            suggestions.style.display = 'none'; // Hide suggestions
            return;
        }

        // Fetch group suggestions from the server
        fetch(`/search_groups?query=${encodeURIComponent(input)}`)
            .then(response => response.json())
            .then(groups => {
                suggestions.style.display = 'block'; // Show suggestions if input is not empty

                groups.forEach(group => {
                    const suggestionItem = document.createElement('a');
                    suggestionItem.href = "#";
                    suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                    suggestionItem.innerHTML = `${group.name}`;
                    suggestions.appendChild(suggestionItem);
                });
            })
            .catch(error => console.error('Error fetching group search results:', error));
    }

    // Add the input event listener to the group search input field
    document.getElementById('existingOption').addEventListener('input', showGroupSuggestions);

    // Handle form submission
    detailsForm.addEventListener('submit', (event) => {
        event.preventDefault();

        // Get specialization name
        const specializationName = document.getElementById('name').value.trim();

        // Create the new content for detailsDisplay using template literals
        const detailsDisplayHtml = `
            <div class="group-details-section">
                <div class="fas fa-bars" id="expand-button">
                    <h2 class="course-card-header">${specializationName}</h2>
                    <p id="group-caption" class="caption success-message">New specialization group added to course successfully</p>
                </div>
                <div class="action-buttons">
                    <button class="edit-button action-button">
                        <a id="group-links" class="edit-link" href="#unit-set-page">Edit<i class="fas fa-edit"></i></a>
                    </button>
                    <button class="delete-button action-button">
                        <a id="group-links" class="delete-link" href="#delete-group">Delete<i class="fa fa-trash" aria-hidden="true"></i></a>
                    </button>
                </div>
            </div>`;

        // Show the detailsDisplay section and append the new content
        detailsDisplay.innerHTML = detailsDisplayHtml;
        detailsDisplay.style.display = 'block';

        // Hide the popup
        popup.style.display = 'none';

        // Add event listener for delete button
        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', (event) => {
                event.preventDefault();
                // Remove the parent group-add-section
                const groupSection = button.closest('.group-details-section');
                if (groupSection) {
                    groupSection.remove();
                    detailsDisplay.remove();
                }
            });
        });
    });
});
