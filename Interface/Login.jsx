import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5001/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid email or password');
      }

      const { token } = await response.json();
      localStorage.setItem('token', token); // Store the token
      onLogin(); // Notify App that login succeeded
      navigate('/'); // Redirect to home page
    } catch (err) {
      setError(err.message || 'An error occurred');
    }
  };

  const handleSignupRedirect = () => {
    navigate('/signup');
  };

  return (
    <div className="page-wrapper">
      <div className="login-container">
        <h2>Login</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit">Log In</button>
          <button type="button" onClick={handleSignupRedirect}>
            Sign Up
          </button>
        </form>
        <div className="login-footer">
          <p>
            <a href="/forgot-password">Forgot Password?</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
