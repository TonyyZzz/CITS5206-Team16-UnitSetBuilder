document.addEventListener("DOMContentLoaded", function () {
    // Star/Unstar Toggle
    document.body.addEventListener("click", function (e) {
        if (e.target.closest(".fav-btn")) {
            const button = e.target.closest(".fav-btn");
            const isFav = button.getAttribute("data-fav") === "true";
            const img = button.querySelector("img");

            img.src = isFav ? "/static/image/unstar.png" : "/static/image/star.png";
            button.setAttribute("data-fav", String(!isFav));
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


        // Event listener for making points editable when the edit icon is clicked
    document.body.addEventListener("click", function (e) {
        if (e.target.closest(".edit-icon")) {
            const parent = e.target.closest("p");
            const pointsDisplay = parent.querySelector(".points-value");
            const pointsInput = parent.nextElementSibling;  // Assuming the input follows the paragraph

            // Hide the points span and show the input field
            pointsDisplay.style.display = "none";
            pointsInput.style.display = "inline";
            pointsInput.focus();  // Focus on the input for editing
        }
    });

    // Event listener to save the points when clicking outside the input field
    document.body.addEventListener("click", function (e) {
        if (!e.target.closest(".edit-points-input") && !e.target.closest(".edit-icon")) {
            document.querySelectorAll(".edit-points-input").forEach(function (input) {
                if (input.style.display === "inline") {
                    const pointsDisplay = input.previousElementSibling.querySelector(".points-value");
                    const newValue = input.value;

                    // Update the points display with the new value
                    pointsDisplay.textContent = newValue;

                    // Hide the input and show the updated points
                    input.style.display = "none";
                    pointsDisplay.style.display = "inline";

                    // Optionally add AJAX here to save the new value to the backend
                }
            });
        }
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
        const groupId = parseInt(modal.getAttribute('data-group-id'),10)
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
                    const unitElement = createUnitElement(unit);
                    saveUnitToGroup(unit, groupId, unitElement);
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

      // Function to create a unit element without adding it to the DOM
    function createUnitElement(unit) {
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
        return unitElement;
    }

    // Function to add the selected unit to the unit set
    function addUnitToSet(unit, groupId) {
        // Create a new unit element (customize this as needed)
        const targetGroup = document.querySelector(`.unit-group[data-group-id="${groupId}"]`);

        if (targetGroup){
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
    // Function to send the selected unit to the backend to be saved and add it to the DOM
    function saveUnitToGroup(unit, groupId, unitElement) {
        fetch('/addUnit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                group_id: groupId,
                unit_id: unit.id
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Unit added successfully");
                unitElement.setAttribute('data-key', data.element_id);

                // Add the unit to the DOM
                const targetGroup = document.querySelector(`.unit-group[data-group-id="${groupId}"]`);
                if (targetGroup) {
                    const binIcon = targetGroup.querySelector('.bin-icon');
                    targetGroup.insertBefore(unitElement, binIcon);

                    // Recalculate points only for core group
                    if (targetGroup.classList.contains('core-unit')) {
                        recalculateCoreGroupPoints(groupId);
                    }
                }
            } else {
                console.error("Error adding unit:", data.error);
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
        <p>Take all units from this group (<span class="points-value">24</span> points)
            <img src="static/image/edit.png" alt="Edit Icon" class="edit-icon">
        </p>
        <input type="text" class="edit-points-input" value="24" size="2" style="display:none;">
        <img src="static/image/bin.png" alt="Delete Section Icon" class="bin-icon">
    `;

    // Append the new group to the unit set container
    unitSet.appendChild(newGroup);
    return newGroup;
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

// Function to recalculate Core Group points automatically
function recalculateCoreGroupPoints(groupId) {
    fetch(`/calculate_points/${groupId}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const group = document.querySelector(`.unit-group[data-group-id="${groupId}"]`);
            if (group) {
                const totalPoints = data.total_points;
                const pointsText = group.querySelector(".points-value");
                const pointsInput = group.querySelector(".edit-points-input");

                // Update the points in the DOM
                pointsText.textContent = totalPoints;
                pointsInput.value = totalPoints;
            }
        } else {
            console.error("Error calculating points:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Function to add a unit to the Core group and update points after the DOM is modified
function addUnitToSet(unit, groupId) {
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
        const binIcon = targetGroup.querySelector('.bin-icon');

        // Insert the unit into the DOM first
        targetGroup.insertBefore(unitElement, binIcon);

        // Recalculate the points only after the unit is added to the DOM
        if (targetGroup.classList.contains('core-unit')) {
            recalculateCoreGroupPoints(groupId);  // Ensure points are recalculated after the DOM update
        }

        return unitElement;
    } else {
        console.error(`Group with ID ${groupId} not found.`);
    }
}

// Use event delegation on the .unit-set container
document.querySelector('.unit-set').addEventListener("click", function (e) {
    if (e.target.closest(".remove-btn")) {
        const button = e.target.closest(".remove-btn");
        const unitElement = button.closest('.unit');
        const groupElement = button.closest('.unit-group');

        console.log("Unit element found:", unitElement);
        console.log("Group element found:", groupElement);

        const groupId = groupElement ? groupElement.getAttribute('data-group-id') : null;
        const dataKey = unitElement ? unitElement.getAttribute('data-key') : null;

        console.log("Removing unit. Unit element:", unitElement);
        console.log("Group element:", groupElement);
        console.log("Group ID:", groupId);
        console.log("Data key:", dataKey);

        if (unitElement && groupId && dataKey) {
            // Send an AJAX request to delete the unit from the database
            fetch('/delete_unit', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    unit_id: dataKey,
                    group_id: groupId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Unit deleted successfully from the database.");
                    unitElement.remove();

                    // Recalculate points for the group after removing the unit
                    recalculateCoreGroupPoints(groupId);
                } else {
                    console.error("Error deleting unit:", data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            console.error("Missing data for unit removal. Unit element:", unitElement, "Group ID:", groupId, "Data key:", dataKey);

            if (groupElement) {
                console.log("Group element HTML:", groupElement.outerHTML);
            } else {
                console.error("Group element not found");
                console.log("Clicked element:", e.target);
                console.log("Button element:", button);
                console.log("DOM structure:", this.outerHTML);
            }
        }
    }
});

   // New function to initialize group points
    function initializeGroupPoints() {
        const groups = document.querySelectorAll('.unit-group');
        groups.forEach(group => {
            const groupId = group.getAttribute('data-group-id');
            if (groupId) {
                recalculateCoreGroupPoints(groupId);
            }
        });
    }

    // Modified recalculateCoreGroupPoints function
    function recalculateCoreGroupPoints(groupId) {
        console.log("Calculating points for group:", groupId);
        fetch(`/calculate_points/${groupId}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Received data from calculate_points:", data);
            if (data.success) {
                const group = document.querySelector(`.unit-group[data-group-id="${groupId}"]`);
                if (group) {
                    const totalPoints = data.total_points;
                    const pointsText = group.querySelector(".points-value");
                    const pointsInput = group.querySelector(".edit-points-input");

                    if (pointsText && pointsInput) {
                        console.log("Updating points for group", groupId, "to", totalPoints);
                        // Update the points in the DOM
                        pointsText.textContent = totalPoints;
                        pointsInput.value = totalPoints;
                    } else {
                        console.error("Points elements not found in group:", groupId);
                    }
                } else {
                    console.error("Group element not found for ID:", groupId);
                }
            } else {
                console.error("Error calculating points:", data.error);
            }
        })
        .catch(error => console.error("Error in recalculateCoreGroupPoints:", error));
    }

    // Call initializeGroupPoints when the page loads
    initializeGroupPoints();

});

