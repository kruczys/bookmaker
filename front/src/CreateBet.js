import React, {useContext, useState} from 'react';
import {UserContext} from "./UserContext";
import axios from "axios";

const CreateBet = ({ onNewBet }) => {
    const {user} = useContext(UserContext)
    const [bet, setBet] = useState(null)
    const [title, setTitle] = useState('')
    const [resolveDateTime, setResolveDateTime] = useState('')

    const createBet = async (betData) => {
        try {
            const response = await axios.post("http://localhost:8000/bets", betData)
            setBet(response.data)
            onNewBet(response.data)
        } catch (error) {
            console.error(error);
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        let resolveDate = new Date(resolveDateTime);
        resolveDate.setHours(resolveDate.getHours() + 1);
        createBet({
            creator_username: user.username,
            title,
            resolve_date: resolveDate,
        });
        setTitle('');
        setResolveDateTime('');
    }

    if (!user) {
        return null;
    }

    return (
        <div>
            <h3>Dodaj swoj zaklad</h3>
            <form onSubmit={handleSubmit}>
                <label>
                    Tytul:
                    <input type="text" value={title} onChange={e => setTitle(e.target.value)} required/>
                </label>
                <label>
                    Data i godzina rozstrzygniecia:
                    <input type="datetime-local" value={resolveDateTime}
                           onChange={e => setResolveDateTime(e.target.value)} required/>
                </label>
                <input type="submit" value="Stworz zaklad"/>
            </form>
        </div>
    );
}

export default CreateBet;