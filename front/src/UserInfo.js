import React, { useContext } from 'react';
import { UserContext } from './UserContext';

const UserInfo = () => {
    const { user, logout } = useContext(UserContext);

    return (
        <div>
            {user ? (
                <div>
                    <p>Username: {user.username}, Balance: {user.balance}</p>
                    <button onClick={() => logout(user.username)}>Logout</button>
                </div>
            ) : (
                <p>No user logged in</p>
            )}
        </div>
    );
};

export default UserInfo;