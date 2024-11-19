/*
    Team15/client/src/pages/landing.js
    This is the landig page. When the user is logged in, they will
    see this page. If they are not logged in, they will be redirected.
*/

import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import ProfileContext from '../context/profileContext';
import AuthContext from '../context/authContext';
import { Posts } from '../components/posts';
import { useNavigate } from 'react-router-dom'

const apiUrl = process.env.REACT_APP_API_URL;

export const Landing = () => {
    
    const navigate = useNavigate()

    const { profile, getProfile } = useContext(ProfileContext);
    const { authTokens } = useContext(AuthContext);

    const [postFeed, setPostFeed] = useState([]);
    const [categories, setCategories] = useState([]);
    const [tags, setTags] = useState([]);

    const [newPost, setNewPost] = useState({
        title: '',
        content: '',
        author: 0,
        tags: [],
        category: ''
    });

    const getPostFeed = async () => {
        const postFeed = await axios.get(`${apiUrl}/api/post/all/`)
            .catch(error => console.error("There was a problem fetching posts from the API", error));
        
        const postCategories = await axios.get(`${apiUrl}/api/categories/`)
            .catch(error => console.error("There was a problem fetching categories from the API", error));

        const postTags = await axios.get(`${apiUrl}/api/tags/`)
            .catch(error => console.error("There was a problem fetching tags from the API", error));
        
        setPostFeed(postFeed.data);
        setCategories(postCategories.data);
        setTags(postTags.data);
    };

    useEffect(() => {
        getPostFeed();
    }, []);

    const handleInputChange = (event) => {
        event.preventDefault();
        setNewPost({ ...newPost, [event.target.name]: event.target.value });
    };

    const handleCategoryChange = (event) => {
        event.preventDefault();
        setNewPost({ ...newPost, category: event.target.value });
    };

    const handleTagsChange = (event) => {
        event.preventDefault();
        const value = Array.from(event.target.selectedOptions, option => option.value);
        setNewPost({ ...newPost, tags: value });
    };

    const setAuthor = () => {
        setNewPost({ ...newPost, author: profile.id});
    };

    const handleFormSubmit = (event) => {
        event.preventDefault();
        setAuthor();
        
        const payload = {
            ...newPost,
            tag_ids: newPost.tags
        };

        axios.post(`${apiUrl}/api/post/create/`, payload, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
            .then(postJSON => setPostFeed([...postFeed, postJSON.data]))
    };

    return (
        <div className="posts-container">
            
            < Posts postData={postFeed} />

            <form onSubmit={handleFormSubmit} className="post-form">
                <input
                    type="text"
                    name="title"
                    value={newPost.title}
                    onChange={handleInputChange}
                    placeholder="Title"
                    required
                />
                <textarea
                    name="content"
                    value={newPost.content}
                    onChange={handleInputChange}
                    placeholder="Content"
                    required
                />
                <div className='post-form-select-container'>
                    <select name="category" onChange={handleCategoryChange}>
                        <option value="">Select a Category</option>
                        {categories.map(category => (
                            <option key={category.id} value={category.id}>{category.name}</option>
                        ))}
                    </select>
                    <select name="tags" onChange={handleTagsChange}>
                        <option value="">Select Tag</option>
                        {tags.map(tag => (
                            <option key={tag.id} value={tag.id}>{tag.name}</option>
                        ))}
                    </select>
                </div>
                <button type="submit">Create Post</button>
            </form>

        </div>
    );
};