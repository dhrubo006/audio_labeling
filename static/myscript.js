// Function to fetch and display a random label
function getRandomLabel() {
    fetch('/get_random_label')
        .then(response => response.json())
        .then(data => {
            const currentLabel = data.label;
            const currentLabelElement = document.getElementById('currentLabel');
            currentLabelElement.textContent = `Current Label: ${currentLabel}`;
        })
        .catch(error => console.error('Error:', error));
}




// Function to show the confirmation dialog
function showConfirmation() {
    const confirmYes = document.getElementById('confirmYes');
    const confirmNo = document.getElementById('confirmNo');
    const submitButton = document.getElementById('submitButton');

    // Show confirmation buttons
    confirmYes.style.display = 'inline-block';
    confirmNo.style.display = 'inline-block';

    // Disable the original submit button
    submitButton.disabled = true;
}


// Function to handle the confirmation
function handleConfirmation() {
    const labelForm = document.getElementById('labelForm');
    const confirmYes = document.getElementById('confirmYes');
    const confirmNo = document.getElementById('confirmNo');

    // Show confirmation buttons
    confirmYes.style.display = 'inline-block';
    confirmNo.style.display = 'inline-block';

    // Disable the original submit button
    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = true;

    // Handle "Yes" click
    confirmYes.addEventListener('click', function () {
        // You can add code here to proceed with the submission
        labelForm.submit(); // This submits the form
    });

    // Handle "No" click
    confirmNo.addEventListener('click', function () {
        // User canceled the submission, so hide the confirmation buttons
        confirmYes.style.display = 'none';
        confirmNo.style.display = 'none';

        // Re-enable the original submit button
        submitButton.disabled = false;
    });
}

// Attach the handleConfirmation function to the form submission
const labelForm = document.getElementById('labelForm');
labelForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    handleConfirmation();
});


// Call the function to fetch and display a random label
getRandomLabel();