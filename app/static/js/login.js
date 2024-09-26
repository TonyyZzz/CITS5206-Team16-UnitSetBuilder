// Ensure the DOM is fully loaded before running scripts
$(document).ready(function() {
    // Handle form submission
    $('#login-form').on('submit', function(event) {
        // Prevent the default form submission behavior (page reload)
        event.preventDefault();

        // Get the values from the username and password fields
        const username = $('#username').val();
        const password = $('#password').val();

        // Make an AJAX request to the backend for login validation
        $.ajax({
            url: '/login',  // Backend route to handle login
            type: 'POST',
            contentType: 'application/json',  // Data format
            data: JSON.stringify({ username: username, password: password }),  // Send form data
            success: function(response) {
                // If login is successful, display a message and redirect the user
                $('#login-message').text(response.message);
                if (response.status === "success") {
                    alert("Login successful! Redirecting to homepage.");
                    window.location.href = "/";  // Redirect to homepage or dashboard
                }
            },
            error: function(xhr) {
                // Handle login failure (e.g., wrong username or password)
                $('#login-message').text(xhr.responseJSON.message);
            }
        });
    });
});
