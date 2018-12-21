import React from 'react'

const Detail = ({address,subscriberURL,handleChange,subscribers,submitFunc,error,loading}) => (
    <div className="container">
      { !loading ? 
        <div className="modal fade " id="exampleModalCenter" tabIndex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="exampleModalCenterTitle">Modal title</h5>
                <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div className="modal-body">
                working....
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" className="btn btn-primary">Save changes</button>
              </div>
            </div>
          </div>
        </div>
        :
        <div display="none"></div>    
      }
        { error ? 
          <div className="alert alert-danger">
            <h4 className="alert-heading">Error</h4>
            <p>{error}</p>
          </div>
          :
          <br/>
        }
        <h2>
        <a target="_blank" rel="noopener noreferrer" href={"https://kovan.etherscan.io/address/"+address+"#code"}>{address}</a>
        </h2>
        <div>
          <p>This device allows you to subscribe to data streams by entering into a smart contract with it.</p>
          <p>If you would like to subscribe to the data produced by this contract enter in your callback URL below.
          </p>
          <div>
            <form className="form">
              <div className="form-group">
                <input type="text" onChange={handleChange} className="form-control" id="subscriberURL" value={subscriberURL} placeholder="https://example.com/mycallback" />
              </div>
            </form>
            <button className="btn btn-primary btn-lg right" onClick={submitFunc}>
              Subscribe
            </button>
            <br/>
          </div>
          <br/>
        </div>
        <div className="alert alert-success">
          <h4 className="alert-heading">Current Subscribers</h4>
          { subscribers.map((s, i) => 
            <div className="" key={i}>{s}</div>
            )
          }
        </div>
    </div>
);

export default Detail
