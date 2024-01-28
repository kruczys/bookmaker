import React, {useContext, useEffect, useState} from 'react';
import { UserContext } from './UserContext';
import axios from 'axios';
import mqtt from "mqtt";

const UserInfo = () => {
    const { user, logout, setUser } = useContext(UserContext);
    const [showForm, setShowForm] = useState(false);
    const [newPassword, setNewPassword] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [balanceAmount, setBalanceAmount] = useState("");
    const [balanceOperation, setBalanceOperation] = useState("increase");
    const client  = mqtt.connect('mqtt://localhost:1883');

    useEffect(() => {
        client.on('connect', function () {
            client.subscribe('user/balanceChanged', function (err) {
                if (err) {
                    console.log('Could not subscribe to topic user/balanceChanged');
                }
            });
        });

        client.on('message', function (topic, message) {
            const balanceChangeInfo = JSON.parse(message.toString());
            if(balanceChangeInfo.userId === user?.id) {
                setUser({
                    ...user,
                    balance: balanceChangeInfo.newBalance,
                });
            }
        });

        return () => {
            if(client) {
                client.end();
            }
        };
    }, [user]);

    const deleteUserAccount = async () => {
        logout(user.username);
        axios.post(`/auth/logout/?username=${user.username}`)
            .then((response) => {
                if(response.status === 200) {
                    axios.delete(`/auth/delete/${user.id}`)
                        .then(() => {
                            console.log('User deleted');
                        })
                        .catch(error => console.log('Account deletion failed:', error));
                }
            })
            .catch(error => console.log('Logout failed:', error));
    };

    const updateUserPassword = async e => {
        e.preventDefault();
        await axios.post(`/auth/password/reset/?user_id=${user.id}&old_password=${oldPassword}&new_password=${newPassword}`);
        setOldPassword("");
        setNewPassword("");
    };

    const updateUserBalance = async () => {
        await axios.put(`/auth/update_balance/${user.id}/${balanceAmount}/${balanceOperation}`);
        setBalanceAmount("");
    };

    return (
        <div>
            {user ? (
                <div>
                    <p>Twoj nick: {user.username}, Portfel: {user.balance}</p>
                    <button onClick={() => logout(user.username)}>Wyloguj</button>
                    <button onClick={() => setShowForm(!showForm)}>Zmien haslo lub usun konto</button>
                    {showForm && (
                        <div>
                            <form onSubmit={updateUserPassword}>
                                <input type="password" value={oldPassword} onChange={e => setOldPassword(e.target.value)} placeholder="Stare haslo" />
                                <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} placeholder="Nowe haslo" />
                                <button type="submit">Zmien haslo</button>
                            </form>
                            <input type="number" value={balanceAmount} onChange={e => setBalanceAmount(e.target.value)} placeholder="Wpisz ilosc pieniedzy" />
                            <select value={balanceOperation} onChange={e => setBalanceOperation(e.target.value)}>
                                <option value="increase">Zwieksz</option>
                                <option value="decrease">Zmniejsz</option>
                            </select>
                            <button onClick={updateUserBalance}>Zmodyfikuj portfel</button>
                            <button onClick={deleteUserAccount}>Usun konto</button>
                        </div>
                    )}
                </div>
            ) : null}
        </div>
    );
};

export default UserInfo;