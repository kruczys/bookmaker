import React, { useContext, useState } from 'react';
import axios from 'axios';
import {UserContext} from "./UserContext";

const SelectedBet = ({ bet, onBetUpdated }) => {
    const { user } = useContext(UserContext); // Assuming UserContext provides the user id
    const [amount, setAmount] = useState(0);
    const [option, setOption] = useState('');
    const [commentText, setCommentText] = useState('');

    const handleUserBet = (e) => {
        e.preventDefault();

        const userBet = {
            user_id: user.id,
            bet_id: bet.id,
            amount: amount,
            option: option,
            resolved: false,
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

    return (
        <div>
            <form onSubmit={handleUserBet}>
                <label>
                    Amount:
                    <input type="number" value={amount} onChange={(e) => setAmount(parseFloat(e.target.value))} required />
                </label>
                <label>
                    Option:
                    <input type="number" value={option} onChange={(e) => setOption(parseInt(e.target.value))} required />
                </label>
                <input type="submit" value="Add UserBet" />
            </form>

            {bet.comments && (<div>
                    <h4>Comments for {bet.title}:</h4>
                    <ul>
                        {bet.comments.map((comment, index) => (
                            <li key={index}>{comment.text} - by {comment.creator_username} {comment.create_date}</li>
                        ))}
                        <form onSubmit={handleComment}>
                            <label>
                                New Comment:
                                <input type="text" value={commentText} onChange={(e) => setCommentText(e.target.value)} required />
                            </label>
                            <input type="submit" value="Post Comment" />
                        </form>
                    </ul>
                </div>
            )}
        </div>
    )
}

export default SelectedBet;