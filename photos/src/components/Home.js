import React from 'react'

const Home = ({photos,uploadFunc, preview}) => (
    <div className="container">
        <p className="lead">
          Welcome to your photo album!
        </p>
        <div>
          <img src={preview} height="200" alt="uploaded"/>
        </div>
        <div className="button-container" >
          <label htmlFor="file-upload" className="plus-icon">
          </label>
          <input id="file-upload" type="file" onChange={uploadFunc}/>
        </div>
    </div>
);

export default Home
