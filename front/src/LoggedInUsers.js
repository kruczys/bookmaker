import React, { useEffect, useState } from 'react';

function LoggedInUsersWebSocketComponent() {
    const [loggedInUsers, setLoggedInUsers] = useState(null);

    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/logged');

        socket.onopen = () => {
            console.log('WebSocket Client Connected');
            socket.send("ping");
        };

        socket.onmessage = (message) => {
            const data = JSON.parse(message.data);
            setLoggedInUsers(data.user_count);
        };

        return () => {
            socket.close();
        };
    }, []);

    if (loggedInUsers === null) return <div>Fetching number of logged in users...</div>;
    return (
        <div>
            Number of logged in users: {loggedInUsers}
        </div>
    );
};

export default LoggedInUsersWebSocketComponent;