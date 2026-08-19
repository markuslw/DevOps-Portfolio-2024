import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../context/authContext';

const apiUrl = process.env.REACT_APP_API_URL;

export function ReactionComponent({ postId }) {
    const { authTokens } = useContext(AuthContext);
    const [userReaction, setUserReaction] = useState(null);
    const [reactionData, setReactionData] = useState({
        total_reactions_count: 0,
        sentiment: 'No reactions yet',
        total_comments_count: 0,
    });

    // Fetch the current reaction and reactions count
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${apiUrl}/api/posts/get_reaction/${postId}/`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                });
                setUserReaction(response.data.user_reaction);
                setReactionData({
                    total_reactions_count: response.data.total_reactions_count || 0,
                    sentiment: response.data.sentiment,
                    total_comments_count: response.data.total_comments_count || 0,
                });
            } catch (error) {
                console.log('Error fetching reaction data:', error);
                setUserReaction(null);
                setReactionData({
                    total_reactions_count: 0,
                    sentiment: 'No reactions yet',
                    total_comments_count: 0,
                });
            }
        };

        fetchData();
    }, [postId, authTokens]);

    const handleReaction = async (event, reactionType) => {
        event.stopPropagation();
        try {
            const response = await axios.post(`${apiUrl}/api/posts/react/${postId}/`, { 'type': reactionType }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authTokens.access}`
                }
            });
            setUserReaction(response.data.user_reaction);
            setReactionData(prevData => ({
                ...prevData,
                total_reactions_count: response.data.total_reactions_count || prevData.total_reactions_count,
                sentiment: response.data.sentiment,
            }));
        } catch (error) {
            console.log('Error handling reaction:', error);
        }
    };

    const removeReaction = async (event) => {
        event.stopPropagation();
        try {
            const response = await axios.delete(`${apiUrl}/api/posts/remove_reaction/${postId}/`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authTokens.access}`
                }
            });
            setUserReaction(null);
            setReactionData(prevData => ({
                ...prevData,
                total_reactions_count: response.data.total_reactions_count || prevData.total_reactions_count,
                sentiment: response.data.sentiment,
            }));
        } catch (error) {
            console.log('Error removing reaction:', error);
        }
    };

    return (
        <div>
            <p>{reactionData.total_reactions_count} Reactions, {reactionData.sentiment}, Comments: {reactionData.total_comments_count}</p>
            <button onClick={(e) => handleReaction(e, 'like')}>Like</button>
            <button onClick={(e) => handleReaction(e, 'dislike')}>Dislike</button>
            <p>Your Reaction: {userReaction ? userReaction.type : 'None'}</p>
        </div>
    );
}



