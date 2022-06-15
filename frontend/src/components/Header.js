import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
      return (
        <nav className="navbar navbar-expand-md navbar-dark bg-dark ">
          <div className="navbar-brand" onClick={() => {this.navTo('')}}>Udacitrivia</div>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item active">
                <div className="nav-link" onClick={() => {this.navTo('')}}>List <span className="sr-only">(current)</span></div>
              </li>
              <li className="nav-item">
                <div className="nav-link" onClick={() => {this.navTo('/add')}}>Add Question</div>
              </li>
              <li className="nav-item">
                <div className="nav-link" onClick={() => {this.navTo('/addcategory')}}>Add Catergory</div>
              </li>
    
              <li className="nav-item">
                <div className="nav-link " onClick={() => {this.navTo('/play')}}>Play</div>
              </li>
            </ul>
          </div>
        </nav>
    
      )
    }
    
  }
export default Header;
