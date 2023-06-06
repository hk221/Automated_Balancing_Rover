const http = require('http');
const fs = require('fs');
const WebSocket = require('ws');

// Create a server
const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/data') {
    let data = '';

    // Receive data from the Arduino
    req.on('data', chunk => {
      data += chunk;
    });

    // Process the received data
    req.on('end', () => {
      // Parse the received JSON data
      const number = JSON.parse(data).number;

      // Display the number in the console
      console.log('Received number:', number);

      // Send the number to connected clients
      wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ number }));
        }
      });

      // Send a response back to the Arduino
      res.statusCode = 200;
      res.end('Number received successfully');
    });
  } else if (req.method === 'GET' && req.url === '/') {
    // Serve the HTML page
    fs.readFile('index.html', 'utf8', (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.end('Error reading file');
        return;
      }

      // Send the HTML page as the response
      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/html');
      res.end(data);
    });
  } else {
    // Handle invalid requests
    res.statusCode = 404;
    res.end('Invalid endpoint');
  }
});

// Create a WebSocket server
const wss = new WebSocket.Server({ server });

// When a WebSocket connection is established
wss.on('connection', ws => {
  console.log('WebSocket connection established');

  // When a WebSocket message is received
  ws.on('message', message => {
    console.log('WebSocket message received:', message);
  });

  // When a WebSocket connection is closed
  ws.on('close', () => {
    console.log('WebSocket connection closed');
  });
});

// Start the server on port 3000
server.listen(3000, () => {
  console.log('Server running on port 3000');
  console.log('http://192.168.1.12:3000');
});