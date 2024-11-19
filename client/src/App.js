import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import { AuthProvider } from './context/authContext';
import { ProfileProvider } from './context/profileContext';

import { Login } from './pages/login';
import { Landing } from './pages/landing';
import { Profile } from './pages/profile';
import { Header } from './components/header';
import { PostDetails } from './pages/postDetails';
import { CommentDetails } from './pages/commentDetails';
import { Search } from './pages/search';
import { Error } from './pages/error';

import { PrivateRoute } from './utils/route';
import { PublicProfile } from './pages/publicProfile';

function App() {

  return (
    <div className="App">
      <Router>
        <AuthProvider>
          <ProfileProvider>
            <Header />
            <Routes>

              <Route path="/" element={
                <PrivateRoute>
                  <Landing />
                </PrivateRoute>} />

              <Route path="/search" element={
                <PrivateRoute>
                  <Search />
                </PrivateRoute>} />
              
              <Route path="/profile" element={
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>} />
              
              <Route path="/username/:pubUsername" element={
                <PrivateRoute>
                  <PublicProfile />
                </PrivateRoute>} />
              
              <Route path="/username/:pubUsername/comment/:commentId" element={
                <PrivateRoute>
                  <CommentDetails/>
                </PrivateRoute>} />
              
              <Route path="/username/:pubUsername/post/:postId" element={
                <PrivateRoute>
                  <PostDetails />
                </PrivateRoute>} />
              
              <Route path="/login" element={<Login />} />
              <Route path="/error" element={<Error />} />
            </Routes>
          </ProfileProvider>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;