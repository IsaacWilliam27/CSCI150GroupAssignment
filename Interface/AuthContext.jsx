import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Restore user from localStorage token
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      axios
        .get('http://localhost:5001/api/profile') // Validate the token
        .then((response) => {
          setUser(response.data.user); // Set user if token is valid
          console.log('User restored from token:', response.data.user);
        })
        .catch(() => {
          setUser(null);
          localStorage.removeItem('token'); // Remove invalid token
        });
    }
  }, []);

  const login = async (credentials) => {
    try {
      const response = await axios.post('http://localhost:5001/api/login', credentials);
      const token = response.data.token;
      const user = response.data.user;

      if (!user) {
        throw new Error('User data is undefined');
      }

      localStorage.setItem('token', token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setUser(user); // Update user state
      console.log('User logged in:', user);
      return true; // Indicate success
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const signup = async (credentials) => {
    await axios.post('http://localhost:5001/api/signup', credentials);
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
