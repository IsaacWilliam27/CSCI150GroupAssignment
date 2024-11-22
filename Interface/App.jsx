import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Header from './Header'; 
import Sidebar from './Sidebar';
import Home from './Home';
import AAPLPage from './AAPLPage'; 
import Login from './Login'; 
import Signup from './Signup'; 

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Track login state

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <Router>
      {!isAuthenticated ? (
        <Routes>
          <Route path="/login" element={<Login onLogin={() => setIsAuthenticated(true)} />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      ) : (
        <div className="grid-container">
          <Header toggleSidebar={toggleSidebar} />
          <Sidebar isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
          <main className={`main-content ${isSidebarOpen ? 'shifted' : ''}`}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/companies/aapl" element={<AAPLPage />} />
            </Routes>
          </main>
        </div>
      )}
    </Router>
  );
}

export default App;
