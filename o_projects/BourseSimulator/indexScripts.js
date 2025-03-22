window.onload = function() {
    fetch('securities.json')
        .then(response => response.json())
        .then(data => {
            // Process the data from the JSON file
            console.log(data);
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            console.error('Error:', error);
        });
}; 


