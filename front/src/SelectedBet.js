import React, {useContext, useState} from 'react';
import axios from 'axios';
import {UserContext} from "./UserContext";

const SelectedBet = ({bet, onBetUpdated, onHideMore}) => {
    const {user} = useContext(UserContext); // Assuming UserContext provides the user id
    const [amount, setAmount] = useState(0);
    const [option, setOption] = useState(0);
    const [commentText, setCommentText] = useState('');

    const handleUserBet = (e) => {
        e.preventDefault();

        const userBet = {
            amount: amount,
            bet_id: bet.id,
            option: option,
            resolved: false,
            user_id: user.id,
        };

        axios.post(`http://localhost:8000/user_bets`, userBet)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    const handleComment = (e) => {
        e.preventDefault();

        const comment = {
            bet_id: bet.id,
            create_date: new Date(),
            creator_username: user.username,
            text: commentText,
        };

        axios.post(`http://localhost:8000/comments/${bet.id}`, comment)
            .then(response => {
                onBetUpdated({...bet, comments: [...bet.comments, response.data]});
                setCommentText('');
            })
            .catch(error => {
                console.log(error);
            });
    }
    if (user) {
        return (
            <div>
                <button onClick={onHideMore}>Powrót</button>
                <h1>{bet.title} </h1>
                <h3>Obstaw</h3>
                <form onSubmit={handleUserBet}>
                    <label>
                        Ilosc:
                        <input type="number" min="1" max={user.balance} value={amount}
                               onChange={(e) => setAmount(parseFloat(e.target.value))}
                               required/>
                    </label>
                    <label>
                        Zaklad:
                        <select value={option} onChange={(e) => setOption(parseInt(e.target.value))} required>
                            <option value="0">Zwycięstwo lewej strony</option>
                            <option value="1">Remis</option>
                            <option value="2">Zwycięstwo prawej strony</option>
                        </select>
                    </label>
                    <input type="submit" value="OBSTAW!"/>
                </form>

                {bet.comments && (<div>
                        <h3>Sekcja komentarzy</h3>
                        <form onSubmit={handleComment}>
                            <label>
                                Dodaj komentarz:
                                <input type="text" value={commentText} onChange={(e) => setCommentText(e.target.value)}
                                       required/>
                            </label>
                            <input type="submit" value="Post Comment"/>
                        </form>
                        {bet.comments.map((comment) => (
                            <>
                                <h4>{comment.creator_username}</h4>
                                <p>{comment.text}</p>
                            </>
                        ))}

                    </div>
                )}
            </div>
        )
    } else {return null;}
}

export default SelectedBet;