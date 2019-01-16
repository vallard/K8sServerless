import React from 'react'

const Home = ({photos,uploadFunc, delFunc}) => (
    <div className="container">
        <p className="lead">
          Welcome to your photo album!
        </p>
        <div className="row">
          {photos.map( (photo, i) => (
            <div className="card card-photo col-sm-3" key={i + "-" + photo.id}>
              { photo.url == null ? 
                  <br/>
                  :
                  <img src={photo.url} className="card-img-top" alt={i + "-" + photo.name} />
              }
              <div className="card-body">
                { photo.date == null ?
                    <br/>
                    :
                    <div className="card-title small">{Date(photo.date).toLocaleString()}</div>
                }
                { photo.objects == null ? 
                    <br/>
                    :
                    <div className="card-text">{photo.objects.toString()}</div>
                }
                <button className="btn btn-sm btn-outline-danger" id={i} onClick={delFunc}>Delete</button>
              </div>
            </div>
          ))}
        </div>
        <div className="button-container" >
          <label htmlFor="file-upload" className="plus-icon">
          </label>
          <input id="file-upload" type="file" onChange={uploadFunc}/>
        </div>
    </div>
);

export default Home
