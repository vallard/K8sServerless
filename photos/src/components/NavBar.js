import React from 'react'
import { BrowserRouter as Router, Route } from "react-router-dom";
import Photos from '../containers/Photos'
//import PhotoDetails from '../containers/PhotoDetails'
import Footer from './Footer'

const NavBar = ({photo}) => (
  <Router >
  <div>
    <nav className="navbar navbar-expand-lg navbar-light">
    <div className="container">
    <a className="navbar-brand" href="/">
      <img className="d-inline-block " alt="photobook" src="images/logo.png" height="20px" />
    </a>
    <span className="navbar-text">
      Photos
    </span>
    <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
      <div className="navbar-nav ml-auto">
        <a className="nav-item nav-link" href="https://github.com/vallard/K8sServerless">
          <i className="fa fa-github" aria-hidden="true"></i>
        </a>
        <a className="nav-item nav-link" href="https://github.com/vallard/K8sServerless">
          <i className="fa fa-file-text-o" aria-hidden="true"></i>
        </a>
      </div>
    </div>
    </div>
  </nav>
    <Route exact path="/photobook/index.html" component={Photos} />
  <Footer />
  </div>
  </Router>
);

export default NavBar
