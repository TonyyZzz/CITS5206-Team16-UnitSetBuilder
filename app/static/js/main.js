/* app/static/js/main.js */
console.log("Main JavaScript file loaded.");
$(document).ready(function() {
    // Expand the navigation menu to show the options
    $('#menu-button').click(function() {
        $('.top-navigation').toggleClass('active');
    });
});

$(document).ready(function() {
    $.ajax({
        url: '/greeting',  // Adjust to your route
        method: 'GET',
        success: function(response) {
            $('#greeting').html(response.message + response.icon);
        },
        error: function() {
            let fallbackMessage = "Hello! Welcome to our site!";
            $('#greeting').html(fallbackMessage); // Fallback in case of error
        }
    });
});