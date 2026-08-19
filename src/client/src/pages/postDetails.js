import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import AuthContext from '../context/authContext';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const apiUrl = process.env.REACT_APP_API_URL;

export const PostDetails = () => {
    const navigate = useNavigate();

    const { pubUsername, postId } = useParams();

    let { authTokens, user } = useContext(AuthContext);

    const [post, setPost] = useState(null);
    const [comments, setComments] = useState([]);

    const [newComment, setNewComment] = useState({
        post: postId,
        content: '',
        author: user.id, // hente ID lagde issues
    });

    const getStuff = async () => {
        // Get details of the post
        await axios.get(`${apiUrl}/api/post/${postId}/`)
            .then(res => setPost(res.data))
            .catch(error => console.error("There was an error fetching the post from the API", error));
        
        // Get comments on this post
        await axios.get(`${apiUrl}/api/post/comment/${postId}/`)
            .then(res => setComments(res.data))
            .catch(error => console.error("There was an error fetching the posts comments from the API", error));
    };

    useEffect(() => {
        getStuff();
    }, [postId]);

    if (!post) return <div>Loading...</div>;

    const handleInputChange = (event) => {
        setNewComment({ ...newComment, [event.target.name]: event.target.value });
    };

    const handleFormSubmit = (event) => {
        event.preventDefault();
        axios.post(`${apiUrl}/api/comment/create/`, newComment, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authTokens.access}`
            }
        })
            .then(res => {
                setComments([...comments, res.data]);
                setNewComment({ ...newComment, content: '' });
            })
    };

    return (
        <div className='post-details-container'>
            <div className='post-details'>
                <img src={`${apiUrl}/api/username/${pubUsername}/img`} alt='placeholder' style={{ marginBottom: '-15px' }} />
                <p style={{ marginBottom: '0px' }}>{post.author.first_name} {post.author.last_name}</p>
            <Link to={`/username/${post.author.username}`}>@{post.author.username}</Link>
                    <h1 style={{ marginTop: '10px' }}>{post.title}</h1>
                <p style={{ margin: '10px 0px 10px 0px' }}>{post.content}</p>
            </div>
            <h2>Comments</h2>
                {comments.map(comment => (
                    <Link to={`/username/${comment.author.username}/comment/${comment.id}`} key={comment.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <div key={comment.id} className="post">
                        <p>By: {comment.author.first_name} {comment.author.last_name}</p>
                        <p>{comment.content}</p>
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
    )
};