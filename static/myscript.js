document.querySelector("form").addEventListener("submit", function(event) {
    let confirmation = confirm("Are you sure you want to submit your labels?");
    if (!confirmation) {
        event.preventDefault();
    } else {
        // Logic to hide the audio clips after submission (You can enhance this as per your needs)
        document.querySelectorAll("audio").forEach(function(audioElement) {
            audioElement.parentElement.style.display = "none";
        });
    }
});
