import { useEffect, useState } from 'react';
import client from '../lib/mqtt';
import socket from '../lib/socket';

export default function Home() {
    const [userCount, setUserCount] = useState(0);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    useEffect(() => {
        client.on('message', (topic, message) => {
            if (topic === 'users/count') {
                setUserCount(message.toString());
            }
        });

        socket.on('chat message', msg => {
            setMessages(messages => [...messages, msg]);
        });

        return () => {
            client.end();
            socket.off('chat message');
        };
    }, []);

    const sendMessageViaSocket = () => {
        socket.emit('chat message', input);
        setInput('');
    };

    return (
        <div>
            <h1>User Count: {userCount}</h1>
            <div>
                <h2>Chat</h2>
                <input value={input} onChange={e => setInput(e.target.value)} />
                <button onClick={sendMessageViaSocket}>Send</button>
                {messages.map((msg, idx) => (
                    <p key={idx}>{msg}</p>
                ))}
            </div>
        </div>
    );
}