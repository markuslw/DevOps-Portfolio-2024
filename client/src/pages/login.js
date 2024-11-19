/*
    Team15/client/src/pages/login.js
    This is the login page. It is the first page that the user
    sees when they open the application.
*/

import React, {useContext, useEffect, useState} from 'react'
import AuthContext from '../context/authContext'
import Logo from '../imgs/logo.webp';
import unAuth from '../imgs/401.jpg';

export const Login = ({ }) => {

    let { loginUser, signUpUser, logState } = useContext(AuthContext)
    let { opacity, setOpacity } = useState(1)
    const [signUp, setSignUp] = useState(false)
    const [submitAllow, setSubmitAllow] = useState(true)

    sessionStorage.removeItem('authTokens')
    sessionStorage.removeItem('profileData')
    
    const toggleLoginSignup = (e) => {
        e.preventDefault();
        if (signUp === false) {
            setSignUp(true)
        } else {
            setSignUp(false)
        }
    }

    const handleSubmit = (e) => {
        if (!submitAllow) return;
        if (signUp === false) {
            loginUser(e)
        } else {
            signUpUser(e)
        }
    }

    useEffect(() => {
        if (logState === 401) {
            setSubmitAllow(false)

            const timeout = setTimeout(() => {
                setSubmitAllow(true);
            }, 1000);

            return () => clearTimeout(timeout);
        }
    }, [logState]);
    
    return (
        <>
            <form className='login-container' onSubmit={handleSubmit}>
                {submitAllow ? (
                        <img className='login-logo' src={Logo} style={{ width: '300px', height: 'auto', opacity: opacity }} />
                    ) : (
                        <img className='login-logo' src={unAuth} style={{ width: '300px', height: '300px', opacity: opacity }} />
                    )}
                    
                <input className='login-field'
                        type='text' name='username' placeholder='Enter username'></input>
                    
                <input className='login-field'
                        type='password' name='password' placeholder='Enter password'></input>
                    
                {signUp ? (
                    <>
                        <input className='login-field'
                        type='text' name='first_name' placeholder='First name'></input>
                    
                        <input className='login-field'
                            type='text' name='last_name' placeholder='Last name'></input>
                        
                        <input className='login-field'
                                type='email' name='email' placeholder='Email'></input>
                    </>
                ) : null}
                    
                    <input 
                        className='login-submit' 
                        type='submit' 
                        value={signUp ? 'Sign up' : 'Log in'}
                        style={{ backgroundColor: submitAllow ? '' : '#B20000' }}
                    />
                <button className='signup-submit' onClick={toggleLoginSignup}>{signUp ? 'Log in instead' : 'Sign up instead'}</button>
            </form>
        </>
    );
};  