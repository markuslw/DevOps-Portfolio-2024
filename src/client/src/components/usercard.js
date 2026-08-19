import React, { useContext, useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;

export const UserCard = ({ dataArr }) => {

    if (!dataArr) return <div />;

    return (
        <div className='usercard-container'>

            {dataArr.users.map(usercard => (
                <div key={usercard.id} className='card-element'>
                    <Link to={`/username/${usercard.username}`} key={usercard.id} style={{ textDecoration: 'none', color: 'inherit' }}> 
                        <div>
                            <img src={`${apiUrl}/api/username/${usercard.username}/img`} alt='placeholder' />
                            <p style={{ marginBottom: '0px' }}>{usercard.first_name} {usercard.last_name}</p>
                            <p className='username-url'>@{usercard.username}</p>
                        </div>
                    </Link>
                </div>
            ))}

            {dataArr.posts.map(post => (

                <div key={post.id} className='card-element'>
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
                                <p style={{
                                overflow: 'hidden',
                                whiteSpace: 'nowrap',
                                textOverflow: 'ellipsis',
                                maxWidth: '20ch' // Limit to 10 characters
                            }}>{post.content}</p>
                            </div>
                        </Link>
                </div>

            ))}
            
        </div>
    )
};