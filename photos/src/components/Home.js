import React from 'react'

const Home = ({photos,uploadFunc, preview}) => (
    <div className="container">
        <p className="lead">
          Welcome to your photo album!
        </p>
        <div>
          {photos.map( (photo, i) => (
            <div className="photo" key={i + "-" + photo.id}>
              <span>{photo.name}</span>
              { photo.date == null ?
                  <span key={"foo-" + i}></span>
                  :
                  <span className="small">{Date(photo.date).toLocaleString()}</span>
              }
              { photo.url == null ? 
                  <br/>
                  :
                  <img src={photo.url} />
              }
            </div>
          ))}
          {preview === "" ? 
            <div/>
            :
            <img src={preview} height="200" alt="uploaded"/>
          }
        </div>
        <div className="button-container" >
          <label htmlFor="file-upload" className="plus-icon">
          </label>
          <input id="file-upload" type="file" onChange={uploadFunc}/>
        </div>
    </div>
);

export default Home
