import React, { Component } from 'react'
import { connect } from 'react-redux'
import Detail from '../components/Detail'
import { withRouter } from 'react-router-dom'
import Loading from '../components/Loading'
import validator from 'validator';

// yikes... 
//https://github.com/ReactTraining/react-router/blob/master/packages/react-router/docs/api/withRouter.md
class ContractDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      subscriberURL : "",
      subscribers : [], // current subscribers
      error : "",
      accounts : [],
      provider: "",
      loading : false,
      working: false,
      workingMessage: ""
    }
  }

  // when the window loads, see if Metamask is there. 
  componentDidMount() {
  }

  /* changing form values */
  handleChange = (event) => {
    const s = this.state
    switch(event.target.id) {
      case "subscriberURL":
        s.subscriberURL = event.target.value;
        break;
      default:
    }
    this.forceUpdate();
  }


  urlIsValid = () => {
    var input = this.state.subscriberURL;
    if(validator.isURL(input.toString())){ 
      return true;
    }
    return false;
  }

   
  subscribe = () => {
  }

  // get the current subscriber URLS from the contract. 
  getSubscribers = () => {
  }




  submitFunc = (event) => {
    if (this.urlIsValid()) {
      const s = this.state
      s.error = ""
      this.forceUpdate()
      this.subscribe()
    }else {
      console.log("is not valid")
      const s = this.state
      s.error = this.state.subscriberURL + " is not a valid URL"
      this.forceUpdate()
    }
  }

  render() {
    return (
    <div>
      <Loading working={this.state.working} workingMessage={this.state.workingMessage} />
      <Detail address={this.props.match.params.contractAddress} 
              subscriberURL={this.state.subscriberURL} 
              error={this.state.error}
              submitFunc={this.submitFunc}
              subscribers={this.state.subscribers}
              loading={this.state.loading}
              handleChange={this.handleChange} />
              
    </div>
    )
  }
}

export default withRouter(connect()(ContractDetails))
