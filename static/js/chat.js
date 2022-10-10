const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
const conversationId = JSON.parse(document.getElementById('conversationId').textContent);

if (!chatLog.hasChildNodes()){
    const emptyText = document.createElement('h3')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'Start a conversation'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // document.querySelector('#chat-log').value += (data.username + ': ' + data.message + '\n');
    const messageElement = document.createElement('div')
    messageElement.innerText = data.message
    messageElement.classList= 'message receiver'
    chatLog.appendChild(messageElement)
    
    if (document.querySelector('#emptyText')){
        document.querySelector('#emptyText').remove()
    }
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInput = document.querySelector('#chat-message-input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': username,
        'conversationId': conversationId,
    }));
    messageInput.value = '';
};