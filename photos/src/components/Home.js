import React from 'react'

const Home = ({photos,uploadFunc}) => (
    <div className="container">
        <p></p>
        <h1 className="header">Photos</h1>
        <p className="lead">Welcome to your photo album!
        </p>
        <div className="button-container" onClick={uploadFunc}>
          <label htmlFor="file-upload" className="plus-icon">
          </label>
          <input id="file-upload" type="file" />
        </div>
    </div>
);

export default Home
