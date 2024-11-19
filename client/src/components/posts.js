import React, { useContext, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import AuthContext from '../context/authContext';
import { ReactionComponent } from '../components/reactionComponent';

const apiUrl = process.env.REACT_APP_API_URL;

export const Posts = ({ postData }) => {

    const { user } = useContext(AuthContext);

    const onDelete = (event) => {
        const response = axios.delete(`${apiUrl}/api/post/${event}/delete`)
            .catch(error => console.error("There was a problem deleting the post", error));
        
        if (!response) {
            return;
        } else {
            return true;
        }
    };

    return (
        <div className='posts-container'>
                {postData.map(post => (
                    <div key={post.id} className="post">
                        <Link to={`/username/${post.author.username}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                            <div>
                                <img src={`${apiUrl}/api/username/${post.author.username}/img`} alt='placeholder' style={{ marginBottom: '-15px' }} />
                                <p style={{ marginBottom: '0px' }}>{post.author.first_name} {post.author.last_name}</p>        
                                <p className="username-url">@{post.author.username}</p>
                            </div>
                        </Link>
                        <Link to={`/username/${post.author.username}/post/${post.id}`} key={post.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                            <div className='post-content'>
                                <h2>{post.title}</h2>
                                <p>{post.content}</p>
                            </div>
                         
                        </Link>
                        <ReactionComponent postId={post.id} /> 
                        

                        {post.author.username === user.username && (
                            <button onClick={() => onDelete(post.id)}>Delete</button>
                        )} 
                    </div>
                ))}
        </div>
    );
}