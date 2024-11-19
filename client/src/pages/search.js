import React, { useState, useEffect } from 'react';
import { UserCard } from '../components/usercard';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;

export const Search = ( ) => {

    const [searchResults, setSearchResults] = useState(null);
    let [searchInput, setSearchInput] = useState(0);

    const getSearchResults = async (inputValue) => {
        const response = await axios.get(`${apiUrl}/api/search/${inputValue}/`, {
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!response) {
            console.error('No data')
        } else {
            setSearchResults(response.data)
        }
    };

    const handleInput = ( inputValue ) => {
        setSearchInput(inputValue.target.value);

        if (searchInput.length >= 2) {
            getSearchResults(searchInput);
        } else if (searchInput.length < 2) {
            setSearchResults(null)
        }
    }

    return (
        <div className='search-container'>
            <form className='search-bar'>
                <input className='search-bar-input' onChange={handleInput} type='text' name='username' placeholder='Type...'></input>
            </form>

            <UserCard dataArr={searchResults} />
            
        </div>
    )
};