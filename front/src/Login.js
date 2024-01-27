import React, { useContext, useState } from 'react';
import { UserContext } from './UserContext';

const Login = () => {
    const { login } = useContext(UserContext);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        login(username, password);
        setUsername('');
        setPassword('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Login"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Haslo"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Zaloguj</button>
        </form>
    );
};

export default Login;