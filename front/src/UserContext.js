import React, { createContext, useState } from 'react';
import Cookies from 'js-cookie';
import axios from "axios";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(Cookies.get('user') ? JSON.parse(Cookies.get('user')) : null);

    const login = async (username, password) => {
        try {
            const response = await axios.post(`/auth/login/?username=${username}&password=${password}`);
            setUser(response.data);
            Cookies.set('user', JSON.stringify(response.data), { expires: 1 });
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    const logout = async (username) => {
        try {
            await axios.post(`/auth/logout/?username=${username}`);
            setUser(null);
            Cookies.remove('user');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    const signup = async (user) => {
        try {
            const response = await axios.post('/auth/signup', user);
            setUser(response.data);
            Cookies.set('user', JSON.stringify(response.data), { expires: 1 });
        } catch (error) {
            if (error.response && error.response.status === 401) {
                alert("User already exists")
            }
            console.error(error)
        }
    };

    const updateUserPassword = async (oldPassword, newPassword) => {
        try {
            const response = await axios.post(`/auth/password/reset/?user_id=${user.id}&old_password=${oldPassword}&new_password=${newPassword}`);
            setUser({
                ...user,
                password: newPassword
            });
            Cookies.set('user', JSON.stringify(user), { expires: 1 });
        } catch (error) {
            console.error('Password update failed:', error);
        }
    };

    const updateUserBalance = async (balanceAmount, balanceOperation) => {
        try {
            const response = await axios.put(`/auth/update_balance/${user.id}/${balanceAmount}/${balanceOperation}`);
            const updatedBalance = balanceOperation === 'increase' ? user.balance + balanceAmount : user.balance - balanceAmount;
            setUser({
                ...user,
                balance: updatedBalance
            });
            Cookies.set('user', JSON.stringify(user), { expires: 1 });
        } catch (error) {
            console.error('Balance update failed:', error);
        }
    };

    const updateBetTitle = async (betId, newTitle) => {
        try {
            const response = await axios.put(`/bets/${betId}/?new_title=${newTitle}`);
            return response.data;
        } catch (error) {
            console.error('Bet title update failed:', error);
        }
    };

    const updateComment = async (commentId, newText) => {
        try {
            const response = await axios.put(`/comments/${commentId}`, newText);
            return response.data;
        } catch (error) {
            console.error('Comment update failed:', error);
        }
    };

    return (
        <UserContext.Provider value={{
            user, login, logout, signup, updateUserPassword, updateUserBalance, updateBetTitle, updateComment
        }}>
            {children}
        </UserContext.Provider>
    );
};