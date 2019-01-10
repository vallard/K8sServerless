import React, { Component } from 'react'
import { connect } from 'react-redux'
import { getPhotos, delPhoto, upPhoto } from '../actions'
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

  showFile = (e) => {
    const t = this;
    var f = e.target
    var reader = new FileReader();
    reader.onloadend = function() {
      // show the file that was uploaded
    }
    if (f.files[0]) {
      reader.readAsDataURL(f.files[0]); 
    }
  }

  uploadPhoto = (e) =>  {
    const t = this;
    console.log("updated.")
    var f = e.target
    if (f.files[0]) {
      let data = new FormData();
      data.append('file', f.files[0])
      data.append('filename', f.files[0].name )
      this.props.upPhoto(data)
    } 
  }
    
  deletePhoto = (e) => {
    const po = this.state.photos[e.target.id]
    const p = po['_id'].$oid
    console.log("Photo ID: ", p)
    this.props.delPhoto(p)
  }
  
  render() {
    return (
    <div>
      <Home photos={this.state.photos} delFunc={this.deletePhoto} uploadFunc={this.uploadPhoto} />
    </div>
    )
  }
}


const mapStateToProps = (state, ownProps) => ({
  photos: state.photos.photos,
})

const mapDispatchToProps = (dispatch) => ({
  getPhotos: () => dispatch(getPhotos()),
  delPhoto: (id) => dispatch(delPhoto(id)),
  upPhoto: (data) => dispatch(upPhoto(data)),
})


export default connect(
  mapStateToProps,
  mapDispatchToProps)(Photos)
