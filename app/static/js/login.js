// Basic form submission logic
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the normal way
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        alert('Logging in...');  // This can be replaced with actual login logic
    } else {
        alert('Please fill in both fields.');
    }
});
