import React, { useContext } from 'react';
import { UserContext } from './UserContext';

const UserInfo = () => {
    const { user, logout } = useContext(UserContext);

    return (
        <div>
            {user ? (
                <div>
                    <p>Twoj nick: {user.username}, Portfel: {user.balance}</p>
                    <button onClick={() => logout(user.username)}>Logout</button>
                </div>
            ) : null}
        </div>
    );
};

export default UserInfo;