import React, {useContext, useEffect, useState} from 'react';
import axios from 'axios';
import {UserContext} from "./UserContext";
import CreateBet from "./CreateBet";
import SelectedBet from './SelectedBet';


function Bets() {
    const [bets, setBets] = useState([]);
    const [openBets, setOpenBets] = useState([]);
    const [resolvedBets, setResolvedBets] = useState([]);
    const [selectedBet, setSelectedBet] = useState(null);
    const [showMore, setShowMore] = useState(false);
    const [editingBetId, setEditingBetId] = useState(null);
    const [editingCommentId, setEditingCommentId] = useState(null);
    const [newBetTitle, setNewBetTitle] = useState("");
    const [newCommentText, setNewCommentText] = useState("");

    const {user, updateBetTitle, updateComment} = useContext(UserContext);
    const [search, setSearch] = useState([]);
    const [searchResults, setSearchResults] = useState([])
    const searchBetsByTitle = async () => {
        const response = await axios.get(`http://localhost:8000/bets/search?title_substring=${search}`);
        setSearchResults(response.data);
    };

    useEffect(() => {
        if (search !== '') {
            searchBetsByTitle();
        } else {
            setSearchResults(resolvedBets);
        }
    }, [search]);

    useEffect(() => {
        axios.get('http://localhost:8000/bets/unresolved')
            .then(response => {
                setOpenBets(response.data);
            })
            .catch(error => {
                console.log(error);
            });
        axios.get('http://localhost:8000/bets/resolved')
            .then(response => {
                setResolvedBets(response.data);
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

    const handleDelete = (betId) => {
        axios.delete(`http://localhost:8000/bets/${betId}/${user.username}`)
            .then(() => {
                setBets(bets.filter(bet => bet.id !== betId));
            })
            .catch(error => {
                console.log(error);
            });
    };


    const handleUpdatedBet = (updatedBet) => {
        setSelectedBet(updatedBet);
        setShowMore(true);
    }

    const hideMore = () => {
        setShowMore(false);
    }

    const handleNewBet = (newBet) => {
        setOpenBets([...openBets, newBet]);
    }

    const handleBetTitleSubmit = () => {
        updateBetTitle(editingBetId, newBetTitle)
            .then(updatedBet => {
                setOpenBets(openBets.map(b => b.id === updatedBet.id ? updatedBet : b));
                setEditingBetId(null);
            })
            .catch(error => {
                console.log(error);
            });
    }

    return (
        <div>
            {!showMore && (
                <>
                    <CreateBet onNewBet={handleNewBet}/>
                    <h3>Otwarte Zaklady</h3>
                    <ul>
                        {openBets.map(bet => {
                            const options = {
                                year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit',
                                minute: '2-digit'
                            };
                            const resolveDate = new Date(bet.resolve_date).toLocaleString(undefined, options);
                            return (
                                <li key={bet.id}>
                                    {editingBetId === bet.id ? (
                                        <>
                                            <input
                                                type="text"
                                                value={newBetTitle}
                                                onChange={e => setNewBetTitle(e.target.value)}
                                            />
                                            <button onClick={handleBetTitleSubmit}>Edytuj</button>
                                        </>
                                    ) : (
                                        <>
                                            {bet.title} - {resolveDate}
                                            {user && bet.creator_username === user.username && !showMore ? (
                                                <button onClick={() => setEditingBetId(bet.id)}>Edytuj Tytul</button>
                                            ) : null}
                                            {user && !showMore ? (
                                                <button onClick={() => handleBetSelection(bet)}>Szczegóły</button>
                                            ) : null}
                                        </>
                                    )}
                                    {user && bet.creator_username === user.username && !showMore &&
                                        <button onClick={() => handleDelete(bet.id)}>Usun</button>
                                    }
                                </li>
                            );
                        })}
                    </ul>
                </>
            )}
            {showMore && selectedBet &&
                <SelectedBet bet={selectedBet} onBetUpdated={handleUpdatedBet} onHideMore={hideMore}/>}
            {!showMore && (
                <div>
                    <h3>Zamkniete zaklady</h3>
                    <label htmlFor="search">Wyszukaj:</label>
                    <input
                        type="text"
                        id="search"
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                        placeholder="Wpisz tytul"
                    />
                    <ul>
                        {searchResults.map(bet => {
                            return (
                                <li key={bet.id}>
                                    {bet.title} - {bet.result === 0 ? "Zwyciestwo lewej strony" : bet.result === 1 ? "Remis" : "Zwyciestwo prawej strony"}
                                </li>
                            );
                        })}
                    </ul>
                </div>
            )}
        </div>
    )
}

export default Bets;