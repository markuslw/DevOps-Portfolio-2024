/*
    Team15/client/src/context/authContext.js
    This is the context for the profile. It is used to
    keep track of the user's profile informaiton.
*/

import React, { createContext, useState, useContext } from 'react'
import AuthContext from '../context/authContext';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;

const ProfileContext = createContext()
export default ProfileContext;

export const ProfileProvider = ({ children }) => {
    const { authTokens } = useContext(AuthContext);

    const [profile, setProfile] = useState([]);

    const getProfile = async() => {
        let details = await axios.get(`${apiUrl}/api/profile/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
        .catch(error => console.error("There was a problem fetching the profile details from the API", error));

        if (!details) {
            return;
        } else {
            let data = details.data;
            if (details.status === 200) {
                setProfile(data)
                sessionStorage.setItem('profileData', JSON.stringify(profile));
            }
        }
    }

    let contextData = {
        getProfile: getProfile,
        profile: profile,
    }

    return(
        <ProfileContext.Provider value={contextData}>
            {children}
        </ProfileContext.Provider>
    )
};