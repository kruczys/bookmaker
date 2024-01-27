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
        }
    };

    return (
        <UserContext.Provider value={{ user, login, logout, signup }}>
            {children}
        </UserContext.Provider>
    );
};