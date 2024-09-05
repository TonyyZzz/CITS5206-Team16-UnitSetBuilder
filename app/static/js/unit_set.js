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
            const unitId = button.getAttribute("data-unit-id");
            const unitElement = document.getElementById(unitId);

            if (unitElement) {
                unitElement.remove();
            }
        }
    });

    // Delete Section Functionality
    document.body.addEventListener("click", function (e) {
        if (e.target.closest(".bin-icon")) {
            const section = e.target.closest(".unit-group");
            if (section) {
                section.remove();
            }
        }
    });

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
            modal.style.display = "block";
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
                            addUnitToSet(unit);  // Function to add unit
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
    function addUnitToSet(unit) {
        // Create a new unit element (customize this as needed)
        const unitElement = document.createElement("div");
        unitElement.className = "unit";
        unitElement.id = `unit-${unit.id}`;
        unitElement.draggable = true;
        unitElement.innerHTML = `
            <span class="unit-name">${unit.name} (ID: ${unit.id})</span>
            <span class="unit-actions">
                <button class="move-btn"><img src="/static/image/drag_unit.png" alt="Move Icon"></button>
                <button class="remove-btn" data-unit-id="unit-${unit.id}"><img src="/static/image/delete_unit.png" alt="Remove Icon"></button>
            </span>
        `;

        // Append the new unit element to the desired group or location in your DOM
        document.querySelector(".core-unit").appendChild(unitElement);  // Adjust selector as needed
    }
});
