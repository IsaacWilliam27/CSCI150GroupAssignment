import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  BsJustify, BsGrid1X2Fill, BsFillArchiveFill, BsFillGrid3X3GapFill,
  BsPeopleFill, BsListCheck, BsMenuButtonWideFill, BsFillGearFill
} from 'react-icons/bs';
import './Sidebar.css';

function Sidebar() {
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [isCompaniesOpen, setCompaniesOpen] = useState(false);
  const [isReportsOpen, setReportsOpen] = useState(false);

  const toggleSidebar = () => setSidebarOpen(!isSidebarOpen);
  const closeSidebar = () => setSidebarOpen(false);
  const toggleCompanies = () => setCompaniesOpen(!isCompaniesOpen);
  const toggleReports = () => setReportsOpen(!isReportsOpen);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 992) setSidebarOpen(false);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <>
      {!isSidebarOpen && (
        <button className="menu-toggle" onClick={toggleSidebar}>
          <BsJustify className="icon_header" />
        </button>
      )}
      {isSidebarOpen && <div className="overlay" onClick={closeSidebar}></div>}
      <aside className={`sidebar ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <div className='sidebar-title'>
          <div className='sidebar-brand'>
            <BsJustify className='icon_header' /> STOCKS
          </div>
          <span className='icon close_icon' onClick={closeSidebar}>X</span>
        </div>
        <ul className='sidebar-list'>
          <li className='sidebar-list-item'>
            <Link to="/">
              <BsGrid1X2Fill className='icon' /> Dashboard
            </Link>
          </li>
          <li className='sidebar-list-item'>
            <Link to="/stocks">
              <BsFillArchiveFill className='icon' /> Stocks
            </Link>
          </li>
          <li className='sidebar-list-item' onClick={toggleCompanies} style={{ cursor: 'pointer' }}>
            <div>
              <BsFillGrid3X3GapFill className='icon' /> Companies
            </div>
            {isCompaniesOpen && (
              <ul className="submenu submenu-open">
                {/* Link to internal AAPL page */}
                <li className='submenu-item'>
                  <Link to="/companies/aapl">AAPL</Link>
                </li>
                {/* Link to external Yahoo Finance page */}
                <li className='submenu-item'>
                  <a 
                    href="https://finance.yahoo.com/quote/AAPL/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                  >
                    AAPL Yahoo Finance
                  </a>
                </li>
              </ul>
            )}
          </li>
          <li className='sidebar-list-item'>
            <Link to="/customers">
              <BsPeopleFill className='icon' /> Customers
            </Link>
          </li>
          <li className='sidebar-list-item'>
            <Link to="/inventory">
              <BsListCheck className='icon' /> Inventory
            </Link>
          </li>
          <li className='sidebar-list-item' onClick={toggleReports} style={{ cursor: 'pointer' }}>
            <div>
              <BsMenuButtonWideFill className='icon' /> Reports
            </div>
            {isReportsOpen && (
              <ul className="submenu submenu-open">
                <li className='submenu-item'><Link to="#">2018</Link></li>
                <li className='submenu-item'><Link to="#">2019</Link></li>
                <li className='submenu-item'><Link to="#">2020</Link></li>
                <li className='submenu-item'><Link to="#">2021</Link></li>
                <li className='submenu-item'><Link to="#">2022</Link></li>
              </ul>
            )}
          </li>
          <li className='sidebar-list-item'>
            <Link to="/settings">
              <BsFillGearFill className='icon' /> Settings
            </Link>
          </li>
        </ul>
      </aside>
    </>
  );
}

export default Sidebar;
