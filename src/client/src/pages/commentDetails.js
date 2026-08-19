import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import AuthContext from '../context/authContext';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const apiUrl = process.env.REACT_APP_API_URL;

export const CommentDetails = () => {
    const navigate = useNavigate();

    const { commentId } = useParams();

    let { authTokens, user } = useContext(AuthContext);
    
    const [comment, setComment] = useState(null);
    const [subComments, setSubComments] = useState([]);

    const [newComment, setNewComment] = useState({
        content: '',
        author: user.id, //hente ID lagde issues
        parent: commentId,
    });

    const getStuff = async () => {
        axios.get(`${apiUrl}/api/comment/${commentId}/`)
            .then(res => setComment(res.data))
            .catch(error => console.error("There was an error getting the comment", error));
    
        // Fetch comments
        axios.get(`${apiUrl}/api/subComments/${commentId}/`)
            .then(res => setSubComments(res.data))
            .catch(error => console.error("There was an error getting the subcomments", error));
    };

    useEffect(() => {
        getStuff();
    }, [commentId]);

    if (!comment) return <div>Loading...</div>;

    const handleInputChange = (event) => {
        setNewComment({ ...newComment, [event.target.name]: event.target.value });
    };

    const handleFormSubmit = (event) => {
        event.preventDefault();
        axios.post(`${apiUrl}/api/subComments/`, newComment, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authTokens.access}`
            }
        })
            .then(res => {
                setSubComments([...subComments, res.data]);
                setNewComment({ ...newComment, content: '' });
            })
    };

    return (
        <div className='comment-details-container'>
                <div className='comment-details'>
                    <img src={`${apiUrl}/api/username/${comment.author.username}/img`} alt='placeholder' style={{ marginBottom: '-15px' }} />
                    <p style={{ marginBottom: '0px' }}>{comment.author.first_name} {comment.author.last_name}</p>
                    <Link to={`/username/${comment.author.username}`}>@{comment.author.username}</Link>
                <h1 style={{ marginTop: '10px' }}>{comment.title}</h1>
                    <p style={{ margin: '10px 0px 10px 0px' }}>{comment.content}</p>
                </div>
                <h2>Comments</h2>
                {subComments.map(subComment => (
                    <Link to={`/username/${comment.author.username}/comment/${subComment.id}`} key={subComment.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                        <div className="post">
                            <p>By: {subComment.author.first_name} {subComment.author.last_name}</p>
                            <p>{subComment.content}</p>
                        </div>
                    </Link>
                ))}
            <form onSubmit={handleFormSubmit}>
                <textarea
                    name="content"
                    value={newComment.content}
                    onChange={handleInputChange}
                    placeholder="Content"
                    required
                />
                <button type="submit">Submit</button>
            </form>
            
        </div>
    );
};