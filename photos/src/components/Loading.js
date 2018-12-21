import React from 'react'

const Loading = ({working, workingMessage}) => (
  <div>
  { working ? 
    <div className="cover">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-sm-4">
            <div className="card loading">
              <div className="card-body">
                <h5 className="card-title">{workingMessage}</h5>
                <h1 className="display-1">
                  <i className="fa fa-circle-o-notch fa-spin"></i>
                </h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    :
    <div></div>
  }
  </div>
);
export default Loading