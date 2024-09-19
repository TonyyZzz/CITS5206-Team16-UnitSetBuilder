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
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('courseId');

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

        // Fetch specialisation suggestions from the server
        fetch(`/search_specialisations?query=${encodeURIComponent(input)}`)
            .then(response => response.json())
            .then(specialisations => {
                suggestions.style.display = 'block'; // Show suggestions if input is not empty

                specialisations.forEach(specialisation => {
                    const suggestionItem = document.createElement('a');
                    suggestionItem.href = "#";
                    suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                    suggestionItem.innerHTML = `${specialisation.name}`;
                                    // Add click event listener to the suggestion item
                    suggestionItem.addEventListener('click', (event) => {
                        event.preventDefault();
                        addSpecialisationToCourse(specialisation.id, courseId);
                    });
                    suggestions.appendChild(suggestionItem);
                });
            })
            .catch(error => console.error('Error fetching group search results:', error));
    }

    // Add the input event listener to the group search input field
    document.getElementById('existingOption').addEventListener('input', showGroupSuggestions);

    function addSpecialisationToCourse(specializationId, courseId) {
    
        console.log(specializationId, courseId);
        // Make the AJAX request
        fetch('/add-specialisation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                course_id: courseId,
                specialization_id: specializationId
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Update successful:', data.message);
                window.location.reload();

            } else {
                console.log('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

});
