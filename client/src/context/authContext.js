/*
    Team15/client/src/context/authContext.js
    This is the context for the authentication. It is used to
    keep track of the user's login status and handle login and logout.
*/

import { createContext, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';

import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;

const AuthContext = createContext()
export default AuthContext;

export const AuthProvider = ({ children }) => {
    /*
        Instead of setting useState(null), we'll utilize the localStorage to keep the user logged in.
        If we set useState(null), the user will be logged out every time the page is refreshed.
    */
    let [user, setUser] = useState(() => (sessionStorage.getItem('authTokens') ? jwtDecode(sessionStorage.getItem('authTokens')) : null))
    let [authTokens, setAuthTokens] = useState(() => (sessionStorage.getItem('authTokens') ? JSON.parse(sessionStorage.getItem('authTokens')) : null))
    let [logState, setLogState] = useState()

    const navigate = useNavigate();

    const signUpUser = async (e) => {
        e.preventDefault()
        const response = await axios.post(`${apiUrl}/api/users/`, {
            username: e.target.username.value,
            password: e.target.password.value,
            first_name: e.target.first_name.value,
            last_name: e.target.last_name.value,
            email: e.target.email.value,
            profile: {
                biography: 'Undefined',
                location: 'Undefined',
              },
        }, {
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .catch(error => console.error("There was an error registering the user", error));

        if (!response) {
            return;
        }
    }

    /*
        Sends a post request to the backend to log in an existing user.
        We'll set AuthTokens and User info in the useState and localStorage.
        Then we'll navigate to the home page.
    */
    let loginUser = async (e) => {
        e.preventDefault()
        const response = await axios.post(`${apiUrl}/api/token/`, {
            username: e.target.username.value,
            password: e.target.password.value
        }, {
            validateStatus: function (status) {
                return status <= 500;
            },
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .catch(error => console.error("There was an error logging in the user", error));

        if (!response) {
            return;
        } else {
            if (response.status !== 200) {
                setLogState(response.status)
                return;
            }
            let data = response.data
            if (data) {
                sessionStorage.setItem('authTokens', JSON.stringify(data));
                setAuthTokens(data)
                setUser(jwtDecode(data.access))

                navigate('/')
            }
        }
    }

    /*
        Removes the AuthTokens and User info from the useState and localStorage.
        Then we'll navigate to the login page.
    */
    let logoutUser = (e) => {
        e.preventDefault()
        sessionStorage.removeItem('authTokens')
        sessionStorage.removeItem('profileData')
        setAuthTokens(null)
        setUser(null)
        navigate('/login')
    }

    let contextData = {
        user: user,
        authTokens: authTokens,
        loginUser: loginUser,
        logoutUser: logoutUser,
        signUpUser: signUpUser,
        logState: logState
    }

    return(
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}