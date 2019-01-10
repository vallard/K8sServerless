import {
  GOT_PHOTOS,
  ERROR,
  DEL_PHOTO,
  UP_PHOTO,
} from '../actions'

const photos = (state = {
  photos: [],
  error: "",
  photo: "",
  data: "",
  }, action) => {
  switch (action.type) {
    case GOT_PHOTOS:
      return Object.assign({}, state, {
        photos: action.photos
      })
    case ERROR: 
      return Object.assign({}, state, {
        error: action.error
      })
    case DEL_PHOTO:
      return Object.assign({}, state, {
        photo: action.photo
      })
    case UP_PHOTO:
      return Object.assign({}, state, {
        data: action.data
      })
    default:
      return state
  }
}
export default photos
