import React, { Component } from 'react'
import { connect } from 'react-redux'
import { getPhotos } from '../actions'
import Home from '../components/Home'

class Photos extends Component {
  constructor(props) {
    super(props);
    this.state = {
      photos : this.props.photos || [],
      preview: ""
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

  uploadPhoto = (e) =>  {
    const t = this;
    var f = e.target
    //console.log("Name: ", f.value, " Last modified: ", f.lastModifiedDate)
    var reader = new FileReader();
    reader.onloadend = function() {
      t.setState({preview: reader.result})
    }
    if (f.files[0]) {
      reader.readAsDataURL(f.files[0]); 
    }else {
      t.setState({preview: ""})
    } 
  }
    
  
  render() {
    return (
    <div>
      <Home photos={this.state.photos} uploadFunc={this.uploadPhoto} preview={this.state.preview}/>
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
