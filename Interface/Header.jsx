import React, { useState } from 'react';
import { 
  BsFillBellFill, 
  BsFillEnvelopeFill, 
  BsPersonCircle, 
  BsSearch, 
} from 'react-icons/bs';
import './Header.css';
import { useAuth } from './AuthContext'; // Import the AuthContext for logout

function Header({ toggleSidebar }) {
  const { logout } = useAuth(); // Use the logout function from AuthContext
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isMessagesOpen, setIsMessagesOpen] = useState(false);
  const [isCommentsOpen, setIsCommentsOpen] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [comments, setComments] = useState([]); 

  const toggleNotifications = () => {
    setIsNotificationsOpen(!isNotificationsOpen);
    setIsMessagesOpen(false);
    setIsCommentsOpen(false);
  };

  const toggleMessages = () => {
    setIsMessagesOpen(!isMessagesOpen);
    setIsNotificationsOpen(false);
    setIsCommentsOpen(false);
  };

  const toggleComments = () => {
    setIsCommentsOpen(!isCommentsOpen);
    setIsNotificationsOpen(false);
    setIsMessagesOpen(false);
  };

  const handleCommentChange = (e) => {
    setCommentText(e.target.value);
  };

  const handleCommentSubmit = () => {
    if (commentText.trim()) {
      setComments([...comments, commentText]);
      setCommentText('');
    }
  };

  const handleLogout = () => {
    logout(); // Call the logout function from AuthContext
    window.location.reload(); // Reload the page to reset the state
  };

  return (
    <header className="header">
      <div className="header-left">
        <div className="search-box">
          <BsSearch className="search-icon" />
          <input type="text" placeholder="Search..." />
        </div>
      </div>

      <div className="header-right">
        {/* Notifications Icon */}
        <div className={`icon-container ${isNotificationsOpen ? 'active' : ''}`} onClick={toggleNotifications}>
          <BsFillBellFill className="icon" />
          <span className="notification-dot"></span>
          {isNotificationsOpen && (
            <div className="notifications-panel">
              <h4>Notifications</h4>
              <p>No new notifications</p>
            </div>
          )}
        </div>

        {/* Messages Icon */}
        <div className={`icon-container ${isMessagesOpen ? 'active' : ''}`} onClick={toggleMessages}>
          <BsFillEnvelopeFill className="icon" />
          <span className="notification-dot"></span>
          {isMessagesOpen && (
            <div className="messages-panel">
              <h4>Messages</h4>
              <p>No new messages</p>
            </div>
          )}
        </div>

        {/* User Profile Icon with Comment Panel */}
        <div className={`user-profile ${isCommentsOpen ? 'active' : ''}`} onClick={toggleComments}>
          <BsPersonCircle className="icon" />
          {isCommentsOpen && (
            <div 
              className="comments-panel" 
              onClick={(e) => e.stopPropagation()} // Prevents closing when clicking inside the panel
            >
              <h4>Leave a Comment</h4>
              <textarea
                value={commentText}
                onChange={handleCommentChange}
                placeholder="Write your comment..."
              />
              <button onClick={handleCommentSubmit}>Submit</button>

              {/* Display Comments */}
              <div className="comments-list">
                {comments.map((comment, index) => (
                  <div key={index} className="comment-bubble">
                    {comment}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Logout Button */}
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}

export default Header;
