import React, { useContext, useState, useEffect } from 'react';
import ProfileContext from '../context/profileContext';
import AuthContext from '../context/authContext';
import axios from 'axios';
import { Posts } from '../components/posts';
import { useNavigate } from 'react-router-dom'

const apiUrl = process.env.REACT_APP_API_URL;

export const Profile = () => {
    const navigate = useNavigate();
    const { profile, getProfile } = useContext(ProfileContext);
    const { user, authTokens } = useContext(AuthContext);

    const [photo, setPhoto] = useState(null);
    const [editPhoto, setEditPhoto] = useState(false);

    const [editProfile, setEditProfile] = useState(false);
    
    const [ refresh, setRefresh ] = useState(false);
    const [ userPosts, setuserPosts] = useState([]);

    const toggleEditPhoto = (event) => {
        event.preventDefault();
        if (editPhoto === false) {
            setEditPhoto(true)
        } else {
            setEditPhoto(false)
        }
    };

    const toggleEditProfile = (event) => {
        event.preventDefault();
        if (editProfile === false) {
            setEditProfile(true)
        } else {
            setEditProfile(false)
        }
    };

    const handleImageSelect = (event) => {
        event.preventDefault();
        setPhoto(event.target.files[0]);
    };

    const uploadPhoto = (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('photo', photo);

        axios.post(`${apiUrl}/api/profile/img/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })

        setRefresh(true);
    };

    const uploadProfile = (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('biography', event.target.biography.value);

        axios.post(`${apiUrl}/api/profile/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })

        setRefresh(true);
    };

    const getProfilePosts = async () => {
        const response = await axios.get(`${apiUrl}/api/username/${user.username}/posts`)
            .catch(error => console.error("There was a problem fetching profile posts from the API", error));

        if (!response) {
            return;
        } else {
            let data = response.data;
            if (response.status === 200) {
                setuserPosts(data)
            }
        }
    };

    useEffect(() => {
        getProfile();
        getProfilePosts();
        setEditPhoto(false);
        setRefresh(false);
    }, [refresh]);

    if (!profile) return <div>Loading...</div>;

    return (
        <div className='profile-container'>
            <div className='profile'>
                <img src={`${apiUrl}/api/username/${user.username}/img`} alt='placeholder' />
                {editPhoto ? (
                    <>
                        <form onSubmit={uploadPhoto}>
                            <input type='file' name='photo' accept='image/*' onChange={handleImageSelect} />
                            <button className='profile-container-upload' type='submit'>Upload</button>
                        </form>
                    </>
                ) : null}
                <div className='profile-container-button-container'>
                    <button onClick={toggleEditPhoto}>{editPhoto ? 'Cancel' : 'Edit Photo'}</button>
                    <button onClick={toggleEditProfile}>{editProfile ? 'Cancel' : 'Edit Profile'}</button>
                </div>
                <h3>{profile.user.first_name} {profile.user.last_name}</h3>
                <p style={{margin: "-20px 0px 0px 0px"}}>@{user.username}</p>
                <br />
                {editProfile ? (
                    <>
                        <form onSubmit={uploadProfile}>
                            <input  className='profile-container-textform' type='text' name='biography' accept='text/*' />
                            <button className='profile-container-upload' type='submit'>Save</button>
                        </form>
                    </>
                ) : <p style={{ margin: "0px 0px 0px 0px" }}>{profile.biography}</p>}
            </div>
            < Posts postData={userPosts} />
        </div>
    )
};