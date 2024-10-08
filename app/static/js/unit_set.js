document.addEventListener("DOMContentLoaded", function () {
    // Star/Unstar Toggle
    document.body.addEventListener("click", function (e) {
        // Check if the clicked element has the class 'capstone-btn'
        const capstoneButton = e.target.closest(".capstone-btn");
        if (capstoneButton) {
            // Get the closest parent element with the class 'unit'
            const elementDiv = capstoneButton.closest('.unit');
            const elementId = elementDiv.getAttribute('data-key');
    
            // Define the URL for the patch request
            const url = `/toggle_flag/capstone/${elementId}`;
    
            // Prepare the patch request
            fetch(url, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Handle the UI update based on the response
                    if (data.success) {
                        // Toggle the icon
                        const img = capstoneButton.querySelector('img');
                        if (img) {
                            const currentSrc = img.getAttribute('src');
                            img.setAttribute('src', currentSrc === '/static/image/star.png' ? '/static/image/unstar.png' : '/static/image/star.png');
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
    

    // Delete Unit
    document.body.addEventListener("click", function (e) {
        if (e.target.closest(".remove-btn")) {
            const button = e.target.closest(".remove-btn");
            const unitElement = button.closest('.unit');
            const dataKey = unitElement.getAttribute('data-key');
            if (unitElement) {
                unitElement.remove();
                // Send an AJAX request to delete the unit from the database
                fetch('/delete_unit', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'  // Indicates it's an AJAX request
                    },
                    body: JSON.stringify({
                        unit_id: dataKey  // Send the unit ID as part of the request body
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log("Unit deleted successfully from the database.");
                        } else {
                            console.error("Error deleting unit:", data.error);
                            // Optionally handle the error (e.g., show an alert or revert the DOM change)
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        // Optionally handle the error (e.g., show an alert or revert the DOM change)
                    });
            }
        }
    });

    // Delete Section Functionality DELETE GROUP HERE !!!!!!!!!!!!!!!!!!!!!!!
    document.body.addEventListener("click", function (e) {
        if (e.target.closest(".bin-icon")) {
            const section = e.target.closest(".unit-group");
            const groupId = parseInt(section.getAttribute('data-group-id'), 10);  // Assuming the group ID is stored in a data attribute
            console.log(groupId)
            if (groupId) {
                deleteGroup(groupId).then(() => {
                    section.remove(); // Remove from the UI if successful
                }).catch((error) => {
                    console.error("Error deleting group:", error);
                });
            }
        }
    });

    // Function to send delete request to Flask
    async function deleteGroup(groupId) {
        const response = await fetch(`/delete_group/${groupId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',  // Indicates AJAX request
            },
        });

        const data = await response.json();

        if (data.success) {
            console.log("Group deleted successfully");
        } else {
            console.error("Error:", data.error);
            throw new Error(data.error);
        }
    }

    // Drag and Drop Functionality for Groups
    let draggedGroup = null;
    document.querySelectorAll('.drag-group-icon').forEach(icon => {
        icon.addEventListener('dragstart', function (e) {
            draggedGroup = icon.closest('.unit-group');
            setTimeout(() => draggedGroup.style.display = 'none', 0);
        });

        icon.addEventListener('dragend', function (e) {
            setTimeout(() => {
                draggedGroup.style.display = 'block';
                draggedGroup = null;
            }, 0);
        });

        icon.addEventListener('dragover', e => e.preventDefault());

        icon.addEventListener('dragenter', function (e) {
            e.preventDefault();
            draggedGroup.style.border = '2px dashed #ccc';
        });

        icon.addEventListener('dragleave', function (e) {
            draggedGroup.style.border = 'none';
        });

        icon.addEventListener('drop', function (e) {
            draggedGroup.style.border = 'none';
            const targetGroup = e.target.closest('.unit-group');
            if (targetGroup && targetGroup !== draggedGroup) {
                targetGroup.parentNode.insertBefore(draggedGroup, targetGroup.nextSibling);
            }
        });
    });

    // Drag and Drop Functionality for Units
    let draggedUnit = null;
    document.querySelectorAll('.unit').forEach(unit => {
        unit.addEventListener('dragstart', function (e) {
            draggedUnit = unit;
            setTimeout(() => unit.style.display = 'none', 0);
        });

        unit.addEventListener('dragend', function (e) {
            setTimeout(() => {
                draggedUnit.style.display = 'flex';
                draggedUnit = null;
            }, 0);
        });

        unit.addEventListener('dragover', e => e.preventDefault());

        unit.addEventListener('dragenter', function (e) {
            e.preventDefault();
            this.style.border = '2px dashed #ccc';
        });

        unit.addEventListener('dragleave', function (e) {
            this.style.border = 'none';
        });

        unit.addEventListener('drop', function (e) {
            this.style.border = 'none';
            if (this !== draggedUnit) {
                this.parentNode.insertBefore(draggedUnit, this.nextSibling);
            }
        });
    });

    // Add Unit Modal and Search Functionality
    const modal = document.getElementById("addUnitModal");
    const closeBtn = document.querySelector(".close-btn");
    const searchInput = document.querySelector(".search-input");
    const resultContainer = document.querySelector(".search-results-container");

    // Open modal and add event listeners
    document.body.addEventListener("click", function (e) {
        if (e.target.closest(".add-unit-icon")) {
            const unitGroup = e.target.closest(".unit-group");
            modal.style.display = "block";
            modal.setAttribute('data-group-id', unitGroup.getAttribute('data-group-id'))
        }
    });

    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
        resultContainer.innerHTML = "";  // Clear results when closing the modal
    });

    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
            resultContainer.innerHTML = "";  // Clear results when closing the modal
        }
    });

    // Handle search input and show results inline
    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim();
        const groupId = parseInt(modal.getAttribute('data-group-id'), 10)
        if (query.length > 0) { // Ensure input length is sufficient
            fetch(`/search?query=${encodeURIComponent(query)}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'  // Indicate AJAX request
                }
            })
                .then(response => response.json())
                .then(data => {
                    // Clear previous results
                    resultContainer.innerHTML = "";

                    console.log("Search results:", data);  // Debugging: log the data received

                    // Show results inline
                    if (data.length > 0) {
                        data.forEach(unit => {
                            const item = document.createElement("div");
                            item.className = "search-result-item";
                            item.textContent = `${unit.name} (ID: ${unit.id})`;

                            // Add click event to add the selected unit to the unit set
                            item.addEventListener("click", function () {
                                const unitElement = addUnitToSet(unit, groupId);  // Function to add unit
                                saveUnitToGroup(unit, groupId, unitElement); // Function to add unit to database
                                modal.style.display = "none";
                                resultContainer.innerHTML = "";  // Clear results after selection
                            });

                            resultContainer.appendChild(item);
                        });
                    } else {
                        const noResults = document.createElement("div");
                        noResults.className = "no-results";
                        noResults.textContent = "No units found.";
                        resultContainer.appendChild(noResults);
                    }
                })
                .catch(error => console.error('Error fetching search results:', error));
        } else {
            resultContainer.innerHTML = ""; // Clear results if query is too short
        }
    });

    // Function to add the selected unit to the unit set
    function addUnitToSet(unit, groupId) {
        // Create a new unit element (customize this as needed)
        const targetGroup = document.querySelector(`.unit-group[data-group-id="${groupId}"]`);

        if (targetGroup) {
            const unitElement = document.createElement("div");
            unitElement.className = "unit";
            unitElement.id = `unit-${unit.id}`;
            unitElement.draggable = true;
            unitElement.innerHTML = `
                <span class="unit-name">${unit.name} (ID: ${unit.id})</span>
                <span class="unit-actions">
                    <button class="move-btn"><img src="/static/image/drag_unit.png" alt="Move Icon"></button>
                    <button class="remove-btn"><img src="/static/image/delete_unit.png" alt="Remove Icon"></button>
                </span>
            `;


            // Find the bin icon in the target group
            const binIcon = targetGroup.querySelector('.bin-icon');

            // Insert the unit element before the bin icon
            targetGroup.insertBefore(unitElement, binIcon);
            return unitElement

        } else {
            console.error(`Group with ID ${groupId} not found.`);
        }
    }

    // Function to send the selected unit to the backend to be saved
    function saveUnitToGroup(unit, group_id, unitElement) {
        console.log(unit, group_id)
        fetch('/addUnit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'  // Indicate AJAX request
            },
            body: JSON.stringify({
                group_id: group_id,  // Pass the group ID
                unit_id: unit.id    // Pass the selected unit ID
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Unit added successfully");
                    // Optionally show a success message
                    unitElement.setAttribute('data-key', data.element_id)
                } else {
                    console.error("Error adding unit:", data.error);
                    // Optionally show an error message
                }
            })
            .catch(error => console.error('Error:', error));
    }


    // CREATE GROUPS HERE!!!!!!!!!!!!!!!!!!!!!!!!!!
    const groupButtons = document.querySelectorAll('.group-btn');

    groupButtons.forEach(button => {
        button.addEventListener('click', () => {
            const groupType = button.classList[1]; // Gets the group type from the class name
            const newGroup = createGroupContainer(groupType);
            addGroup(itemType, itemData['id'], groupType, newGroup);
        });
    });

    function createGroupContainer(groupType) {
        const unitSet = document.querySelector('.unit-set');

        // Create a new div for the group
        const newGroup = document.createElement('div');
        newGroup.classList.add('unit-group', groupType + '-unit');
        newGroup.innerHTML = `
            <div class="group-header">
                <h3>${capitalizeFirstLetter(groupType.replace('-', ' '))} Unit</h3>
                <div class="group-icons">
                    <img src="static/image/drag_group.png" alt="Drag Group Icon" class="drag-group-icon" draggable="true">
                    <img src="static/image/add_unit.png" alt="Add Unit Icon" class="add-unit-icon">
                </div>
            </div>
            <p>Take all units from this group (24 points)
                <img src="static/image/edit.png" alt="Edit Icon" class="edit-icon">
            </p>
            <!-- Units will be added here -->
            <img src="static/image/bin.png" alt="Delete Section Icon" class="bin-icon">
        `;

        // Append the new group to the unit set container
        unitSet.appendChild(newGroup);
        return newGroup
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    console.log(courseData)
    console.log(itemData)
    // createGroup
    function addGroup(type, item_id, group_type, newGroup) {

        if (type === 'unitset') {
            fetch('/add_group_to_unitset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'  // Indicate AJAX request
                },
                body: JSON.stringify({
                    unit_set_id: item_id,
                    is_specialization: false,
                    group_type: group_type
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log("group added to unitset successfully");
                        // Optionally show a success message
                        newGroup.setAttribute('data-group-id', data.group_id);
                    } else {
                        console.error("Error adding group:", data.error);
                        // Optionally show an error message
                    }
                })
                .catch(error => console.error('Error:', error));
        } else if (type === 'specialization') {
            console.log("I am here")
            fetch('/add_group_to_specialization', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'  // Indicate AJAX request
                },
                body: JSON.stringify({
                    specialization_id: item_id,
                    is_specialization: true,
                    group_type: group_type
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log("group added to specialization successfully");
                        // Optionally show a success message
                        newGroup.setAttribute('data-group-id', data.group_id);
                    } else {
                        console.error("Error adding group:", data.error);
                        // Optionally show an error message
                    }
                })
                .catch(error => console.error('Error:', error));
        }

    }


});
