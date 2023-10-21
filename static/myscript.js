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

// Call the function to fetch and display a random label
getRandomLabel();