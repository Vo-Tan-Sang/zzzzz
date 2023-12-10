   setTimeout(function() {
    var messages = document.querySelectorAll('.custom-alert');
    for (var i = 0; i < messages.length; i++) {
        messages[i].style.display = 'none';
    }
}, 5000); 
// Comments
$(document).ready(function() {
    $(".reply-button").click(function() {
        $(this).next(".reply-form").toggle();
    });
});