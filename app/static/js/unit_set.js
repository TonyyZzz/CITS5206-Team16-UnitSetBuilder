document.addEventListener("DOMContentLoaded", function() {
    // Star -> Unstar
    const favButtons = document.querySelectorAll(".fav-btn");
    favButtons.forEach(button => {
        button.addEventListener("click", function() {
            const isFav = button.getAttribute("data-fav") === "true";
            const img = button.querySelector("img");
            
            if (isFav) {
                img.src = "/static/image/unstar.png";
                button.setAttribute("data-fav", "false");
            } else {
                img.src = "/static/image/star.png";
                button.setAttribute("data-fav", "true");
            }
        });
    });

    // Delete unit
    const removeButtons = document.querySelectorAll(".remove-btn");
    removeButtons.forEach(button => {
        button.addEventListener("click", function() {
            const unitId = button.getAttribute("data-unit-id");
            const unitElement = document.getElementById(unitId);
            
            if (unitElement) {
                unitElement.remove();
            }
        });
    });
});

    // Delete section functionality
    const deleteSectionIcons = document.querySelectorAll(".bin-icon");
    deleteSectionIcons.forEach(icon => {
        icon.addEventListener("click", function() {
            const section = icon.closest(".unit-group"); // Get the closest unit-group section
            if (section) {
                section.remove(); // Remove the entire section
            }
        });
    });

// Function to remove a section
function removeSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.remove();
        console.log('Section removed:', sectionId);  // Debugging line
    } else {
        console.log('Section not found:', sectionId);  // Debugging line
    }
}

// Drag Group
document.addEventListener("DOMContentLoaded", function() {
    let draggedGroup = null;

    // Handle drag start
    document.querySelectorAll('.drag-group-icon').forEach(icon => {
        icon.addEventListener('dragstart', function(e) {
            draggedGroup = icon.closest('.unit-group');
            setTimeout(function() {
                draggedGroup.style.display = 'none';
            }, 0);
        });

        icon.addEventListener('dragend', function(e) {
            setTimeout(function() {
                draggedGroup.style.display = 'block';
                draggedGroup = null;
            }, 0);
        });

        icon.addEventListener('dragover', function(e) {
            e.preventDefault();
        });

        icon.addEventListener('dragenter', function(e) {
            e.preventDefault();
            draggedGroup.style.border = '2px dashed #ccc';
        });

        icon.addEventListener('dragleave', function(e) {
            draggedGroup.style.border = 'none';
        });

        icon.addEventListener('drop', function(e) {
            draggedGroup.style.border = 'none';
            const targetGroup = e.target.closest('.unit-group');
            if (targetGroup && targetGroup !== draggedGroup) {
                targetGroup.parentNode.insertBefore(draggedGroup, targetGroup.nextSibling);
            }
        });
    });
});


// Drag Unit
document.addEventListener("DOMContentLoaded", function() {
    let draggedUnit = null;

    document.querySelectorAll('.unit').forEach(unit => {
        unit.addEventListener('dragstart', function(e) {
            draggedUnit = unit;
            setTimeout(function() {
                unit.style.display = 'none';
            }, 0);
        });

        unit.addEventListener('dragend', function(e) {
            setTimeout(function() {
                draggedUnit.style.display = 'flex';
                draggedUnit = null;
            }, 0);
        });

        unit.addEventListener('dragover', function(e) {
            e.preventDefault();
        });

        unit.addEventListener('dragenter', function(e) {
            e.preventDefault();
            this.style.border = '2px dashed #ccc';
        });

        unit.addEventListener('dragleave', function(e) {
            this.style.border = 'none';
        });

        unit.addEventListener('drop', function(e) {
            this.style.border = 'none';
            if (this !== draggedUnit) {
                this.parentNode.insertBefore(draggedUnit, this.nextSibling);
            }
        });
    });
});


// Add unit
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("addUnitModal");

    const addUnitIcons = document.querySelectorAll(".add-unit-icon");

    const closeBtn = document.querySelector(".close-btn");

    addUnitIcons.forEach(icon => {
        icon.addEventListener("click", function() {
            modal.style.display = "block";
        });
    });

    closeBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});
