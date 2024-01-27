import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Bets() {
    const [bets, setBets] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/bets/unresolved')
            .then(response => {
                setBets(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    return (
        <div>
            <h3>Otwarte Zaklady</h3>
            <ul>
                {bets.map(bet => {
                    const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' };
                    const resolveDate = new Date(bet.resolve_date).toLocaleString(undefined, options);
                    return <li key={bet.id}>{bet.title} - {resolveDate}</li>;
                })}
            </ul>
        </div>
    )
}

export default Bets;