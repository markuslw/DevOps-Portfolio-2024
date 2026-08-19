/*
    Team15/client/src/components/header.js
    This is the header component, it displays Home, Login or Logout
    at the top of the page.
*/

import React, { useContext , useEffect} from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/authContext';
import ProfileContext from '../context/profileContext';

export const Header = ( ) => {
    const { user, logoutUser } = useContext(AuthContext)
    const { profile, getProfile } = useContext(ProfileContext)

    useEffect(() => {
        if (user) {
            getProfile();
        }
    }, [user])

    return (
        <div className='header'>
            <Link className='header-element' to="/">Home</Link>
            {user && <Link className='header-element' to='/profile' >Profile</Link>}
            {user && <Link className='header-element' to='/search'>Search</Link>}
            {user ? (
                <Link className='header-element' onClick={logoutUser}>Logout</Link>
            ) : (
                <Link className='header-element' to="/login" >Login</Link>
            )}
        </div>
    )
};