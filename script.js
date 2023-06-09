// Function to send GET request and update the data on the webpage
function getData() {
    fetch('/acc')
      .then(response => response.text())
      .then(data => {
        document.getElementById('data').textContent = data;
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  
  // Function to periodically update the data
  setInterval(getData, 1000); // Update every 1 second
  