/* app/static/js/main.js */
console.log("Main JavaScript file loaded.");
$(document).ready(function() {
    // Expand the navigation menu to show the options
    $('#menu-button').click(function() {
        $('.top-navigation').toggleClass('active');
    });
});
