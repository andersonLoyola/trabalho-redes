import React, { useContext } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './contexts/AuthContext';
import Login from './pages/Login';
import Home from './pages/Home';
import { Chat } from './pages/Chat';
import { ChatProvider } from './contexts/ChatContext';
import { LoadingProvider } from './contexts/LoadingContext';

function PrivateRoute({ children }) {
  const { token } = useContext(AuthContext);
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <AuthProvider>
      <ChatProvider>
        <LoadingProvider>
          <Router>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/home" element={<PrivateRoute><Home /></PrivateRoute>} />
              <Route path="/chat" element={<PrivateRoute><Chat /></PrivateRoute>} />
              <Route path="*" element={<Navigate to="/home" />} />
            </Routes>
          </Router>
        </LoadingProvider>
      </ChatProvider>
    </AuthProvider>
  );
}

export default App;