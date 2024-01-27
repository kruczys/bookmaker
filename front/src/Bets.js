import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import SelectedBet from './SelectedBet';
import {UserContext} from "./UserContext";
import CreateBet from "./CreateBet";

function Bets() {
    const [bets, setBets] = useState([]);
    const [selectedBet, setSelectedBet] = useState(null);
    const [showMore, setShowMore] = useState(false);
    const {user} = useContext(UserContext)

    useEffect(() => {
        axios.get('http://localhost:8000/bets/unresolved')
            .then(response => {
                setBets(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    const handleBetSelection = (bet) => {
        setSelectedBet({...bet, comments: []});
        setShowMore(true);

        axios.get(`http://localhost:8000/comments/${bet.id}`)
            .then(response => {
                setSelectedBet({...bet, comments: response.data});
            })
            .catch(error => {
                console.log(error);
            });
    }

    const handleUpdatedBet = (updatedBet) => {
        setSelectedBet(updatedBet);
        setShowMore(true);
    }

    const hideMore = () => {
        setShowMore(false);
    }

    const handleNewBet = (newBet) => {
        setBets([...bets, newBet]);
    }

    return (
        <div>
            <CreateBet onNewBet={handleNewBet}/>
            <h3>Otwarte Zaklady</h3>
            <ul>
                {bets.map(bet => {
                    const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit',
                        minute: '2-digit' };
                    const resolveDate = new Date(bet.resolve_date).toLocaleString(undefined, options);
                    return (
                        <li key={bet.id}>
                            {bet.title} - {resolveDate}
                            {user && !showMore? (
                                <button onClick={() => handleBetSelection(bet)}>Szczegóły</button>
                            ) : null}
                        </li>
                    );
                })}
            </ul>
            {showMore && selectedBet && <SelectedBet bet={selectedBet} onBetUpdated={handleUpdatedBet} onHideMore={hideMore} />}
        </div>
    )
}

export default Bets;