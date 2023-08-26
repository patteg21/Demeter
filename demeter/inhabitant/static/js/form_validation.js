document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("demeter-question").addEventListener("submit", function(event) {
        
        var userInput = document.getElementById("user-input").value;

        if (userInput.trim() === "") {
            event.preventDefault();
            alert("Input field is empty");
        } else {
            // The form will submit normally
        }
    });
});
