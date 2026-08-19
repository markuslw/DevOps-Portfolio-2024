/*
    Team15/client/src/utils/route.js
    This is the routing utility. It routes the user to the login page
    if they are not logged in and to the home page if they are.
*/

import { Navigate } from 'react-router-dom'
import { useContext } from 'react'
import AuthContext from '../context/authContext';

export const PrivateRoute = ({ children, ...rest }) => {
    let { user } = useContext(AuthContext)

    return !user ? <Navigate to='/login' /> : children;
};