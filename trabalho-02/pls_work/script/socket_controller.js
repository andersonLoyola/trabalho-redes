document.addEventListener('submit', (event) => {
    event.preventDefault();
});

const socket = new WebSocket('ws://localhost:9090');

socket.onmessage = (event) => {
        const response = JSON.parse(event.data);

        if (response.response_type === 'auth') {
      
            if (response.success) {
                window.location.href = 'home.html';
            } else {
                document.getElementById('error').innerText = response.message;
            }
        }

        if (response.respose_type === 'available_conns') {
            const { connections } = response;
            const connList = document.getElementById('conn-list');
            connections.forEach((connection) => {
                const listItem = document.createElement('li');
                listItem.textContent = connection.name;
                listItem.addEventListener('click', () => {
                    sendConnectionId(connection.id);
                });
                connList.appendChild(listItem);
            })

        }

        if (response.response_type === 'connection_details') {
            const { connection } = response;
        
        }        
    }


socket.onclose = () => {
    console.log('Connection closed');
}




const login  = async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        socket.send(JSON.stringify({
            request_type: 'auth',
            username: username,
            password: password
        }));
    } catch (error) {
        console.trace(error);
    }
};

const getConnectionsDetails = async (connection_id) => {
    try {
        socket.send(JSON.stringify({
            request_type: 'get_connections',
            token: localStorage.getItem('token'),
            connection_id: connection_id

        }));
    } catch (error) {
        console.trace(error);
    }
}

