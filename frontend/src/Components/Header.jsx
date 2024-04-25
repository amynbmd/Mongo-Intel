// In Header.js
import React from 'react';
import { NavLink } from 'react-router-dom';

function Header() {
  return (
    <nav className="navbar navbar-expand-sm navbar-light bg-light">
      <strong>
        <NavLink exact className="navbar-brand" to="/">
          Mongo Intel
        </NavLink>
      </strong>
      <div className="collapse navbar-collapse">
        <ul className="navbar-nav mr-auto">
          <li className="nav-item">
            <NavLink exact className="nav-link" to="/">
              Home
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink exact className="nav-link" to="/area-analysis">
              Predictive Analysis
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink exact className="nav-link" to="/predictive-analysis">
            Area Analysis
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink exact className="nav-link" to="/real-time-tracking">
              Chatbot Platform
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink exact className="nav-link" to="/location">
              Location
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Header;
