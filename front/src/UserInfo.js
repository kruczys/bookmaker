import React, {useContext, useEffect, useState} from 'react';
import {UserContext} from './UserContext';
import axios from 'axios';

const UserInfo = () => {
    const {user, logout} = useContext(UserContext);
    const [showForm, setShowForm] = useState(false);
    const [newPassword, setNewPassword] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [balanceAmount, setBalanceAmount] = useState("");
    const [balanceOperation, setBalanceOperation] = useState("increase");
    const [balance, setBalance] = useState(0);
    const [bets, setBets] = useState([]);

    useEffect(() => {
        if (user) {
            const socket = new WebSocket(`ws://localhost:8000/ws/balance/${user.id}`);
            socket.onopen = function () {
                console.log('WebSocket is open now.');
                setBalance(user.balance)
            };
            socket.onclose = function () {
                console.log('WebSocket is closed now.');
            };
            socket.onerror = function (error) {
                console.log('WebSocket Error: ', error);
            };
            socket.onmessage = function (event) {
                const newBalance = JSON.parse(event.data);
                setBalance(newBalance);
            };
            return () => {
                socket.close();
            };
        }
    }, [user]);

    useEffect(() => {
       fetchUserBets();
    }, [user]);

    const fetchUserBets = async () => {
        if (user) {
            const response = await axios.get(`/user_bets/?user_id=${user.id}`);
            setBets(response.data);
        }
    };

    const deleteUserBet = async (userBetId) => {
        await axios.delete(`/user_bets/${userBetId}`);
        fetchUserBets();
    };


    const deleteUserAccount = async () => {
        logout(user.username);
        axios.post(`/auth/logout/?username=${user.username}`)
            .then((response) => {
                if (response.status === 200) {
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
                    <p>Twoj nick: {user.username}, Portfel: {balance}</p>
                    <button onClick={() => logout(user.username)}>Wyloguj</button>
                    <button onClick={() => setShowForm(!showForm)}>Szczegóły konta</button>
                    {showForm && (
                        <div>
                            <form onSubmit={updateUserPassword}>
                                <input type="password" value={oldPassword}
                                       onChange={e => setOldPassword(e.target.value)} placeholder="Stare haslo"/>
                                <input type="password" value={newPassword}
                                       onChange={e => setNewPassword(e.target.value)} placeholder="Nowe haslo"/>
                                <button type="submit">Zmien haslo</button>
                            </form>
                            <input type="number" value={balanceAmount} onChange={e => setBalanceAmount(e.target.value)}
                                   placeholder="Wpisz ilosc pieniedzy"/>
                            <select value={balanceOperation} onChange={e => setBalanceOperation(e.target.value)}>
                                <option value="increase">Zwieksz</option>
                                <option value="decrease">Zmniejsz</option>
                            </select>
                            <button onClick={updateUserBalance}>Zmodyfikuj portfel</button>
                            <button onClick={deleteUserAccount}>Usun konto</button>
                            <div>
                                <h2>Twoje pieniądze w grze: </h2>
                                {bets.map(bet => (
                                    <div key={bet.id}>
                                        <p>{bet.amount}</p>
                                        <button onClick={() => deleteUserBet(bet.id)}>ZWROT</button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            ) : null}
        </div>
    );
};

export default UserInfo;