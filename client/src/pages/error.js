import React from 'react'

export const Error = ({ }) => {

    sessionStorage.removeItem('authTokens')
    sessionStorage.removeItem('profileData')
    
    return (
        <>
            <div className='error-container'>
                <h1>401</h1>
                <h2>Unauthorized</h2>
            </div>
        </>
    );
};  