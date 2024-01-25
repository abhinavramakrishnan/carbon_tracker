document.querySelector('#chat-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const message = document.querySelector('#message').value;
  
    if (message.trim() === '') {
      console.log('Empty message, not sending to server');
      return;
    }
  
    addMessageToChat('You: ' + message);
  
    fetch('/bot', {
      method: 'POST',
      body: new FormData(event.target)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Data from server:', data);
        addMessageToChat('Terra: ' + data.response);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  
    document.querySelector('#message').value = '';
  });
  
  function addMessageToChat(message) {
    const chatbox = document.querySelector('#chatbox');
    const messageElement = document.createElement('p');
    messageElement.innerHTML = message;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  