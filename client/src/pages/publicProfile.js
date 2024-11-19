import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Posts } from '../components/posts';
import AuthContext from '../context/authContext';


const apiUrl = process.env.REACT_APP_API_URL;

export const PublicProfile = () => {

    const { pubUsername } = useParams();

    const { authTokens } = useContext(AuthContext);

    const [publicUser, setPublicUser] = useState([]);
    const [publicUserPosts, setPublicUserPosts] = useState([]);
    const [followStatus, setFollowStatus] = useState(false);

    const navigate = useNavigate();

    useEffect(() => {
        getFollowStatus();
        getPublicProfile();
        getPublicProfilePosts();
    }, [pubUsername]);

    const getPublicProfile = async () => {
        let profDetails = await axios.get(`${apiUrl}/api/username/${pubUsername}/`, {
            validateStatus: function (status) {
                return status <= 302;
            },
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })

        if (!profDetails) {
            return;
        } else {
            if (profDetails.status === 302) {
                navigate(profDetails.data.Location)
            }
            if (profDetails.status === 200) {
                setPublicUser(profDetails.data)
            }
        }
    };

    const getFollowStatus = async () => {
        const isFollowing = await axios.get(`${apiUrl}/api/username/${pubUsername}/isfollowing`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
        .catch(error => console.error("There was an error fetching the follow status of the user", error));

        setFollowStatus(isFollowing.data.Status);
    }

    const getPublicProfilePosts = async () => {
        const response = await axios.get(`${apiUrl}/api/username/${pubUsername}/posts`)
            .catch(error => console.error("There was a problem fetching public profile posts from the API", error));

        if (!response) {
            return;
        } else {
            let data = response.data;
            if (response.status === 200) {
                setPublicUserPosts(data)
            }
        }
    };

    const followUser = async () => {
        const response = await axios.get(`${apiUrl}/api/username/${pubUsername}/follow`, {
            validateStatus: function (status) {
                return status <= 500;
            },
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        });

        if (!response) {
            return;
        } else if (response.status === 201) {
            setFollowStatus(true);
        
        } else if (response.status === 204) {
            setFollowStatus(false);
        }
    }

    return (
        <div className='profile-container'>
            <div className='profile'>
                <img src={`${apiUrl}/api/username/${pubUsername}/img`} alt='placeholder' />
                <h3>{publicUser.first_name} {publicUser.middle_name} {publicUser.last_name}</h3>
                <p style={{margin: "-20px 0px 0px 0px"}}>@{publicUser.username}</p>
                <br />
                <p style={{ margin: "0px 0px 0px 0px" }}>{publicUser.biography}</p>
                <div className='profile-container-button-container'>
                    <button onClick={followUser}>{followStatus ? 'Unfollow' : 'Follow'}</button>
                </div>
            </div>
            < Posts postData={publicUserPosts} />
        </div>
    )
};