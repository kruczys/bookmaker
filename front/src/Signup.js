import React, {useContext, useState} from 'react';
import {UserContext} from './UserContext';

const Signup = () => {
    const {user, signup} = useContext(UserContext);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            alert("Passwords don't match!");
            return;
        }
        signup({username, password});
        setUsername('');
        setPassword('');
        setConfirmPassword('');
    };

    return (
        <>
            {!user ? (
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>Wpisz swoj login:</label>
                        <input
                            type="text"
                            placeholder="login"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label>Wpisz haslo:</label>
                        <input
                            type="password"
                            placeholder="haslo"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label>Potwierdz haslo:</label>
                        <input
                            type="password"
                            placeholder="haslo"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit">Zarejestruj</button>
                </form>
            ) : null}

        </>

    );
};

export default Signup;