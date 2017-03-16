import React, { Component } from 'react';
import { Link } from 'react-router';

class Layout extends Component {
  render() {
    return (
      <div>
        <nav className="navbar navbar-inverse">
          <div className="container-fluid">
            <div className="navbar-header">
              <a className="navbar-brand" href="#">FitLabs</a>
            </div>
            <ul className="nav navbar-nav">
              <li><Link to="home">Home</Link></li>
              <li><Link to="students">Students</Link></li>
              <li><Link to="teachers">Teachers</Link></li>
              <li><Link to="schools">GB Schools</Link></li>
            </ul>
          </div>
        </nav>
        {this.props.children}
      </div>

    );
  }
}
export default Layout;
