import React, { Component } from 'react'
import { connect } from 'react-redux'
import { getPhotos } from '../actions'
import Home from '../components/Home'

class Photos extends Component {
  constructor(props) {
    super(props);
    this.state = {
      photos : this.props.photos || [],
    }
  }

  componentDidMount() {
    this.props.getPhotos()
  }

  // get more examples: https://github.com/katopz/web3-react-example/blob/master/src/App.js
  componentWillReceiveProps(nextProps) {
    this.setState({
      photos: nextProps.photos || [],
    })
  }

  uploadPhoto() {
    console.log("Uploading photo")
  }

  render() {
    return (
    <div>
      <Home photos={this.state.photos} uploadFunc={this.uploadPhoto}/>
    </div>
    )
  }
}


const mapStateToProps = (state, ownProps) => ({
  photos: state.photos.photos,
})

const mapDispatchToProps = (dispatch) => ({
  getPhotos: () => dispatch(getPhotos()),
})


export default connect(
  mapStateToProps,
  mapDispatchToProps)(Photos)
