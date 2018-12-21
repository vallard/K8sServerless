import {
  GOT_PHOTOS,
  ERROR,
} from '../actions'

const photos = (state = {
  photos: [],
  error: "",
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
    default:
      return state
  }
}
export default photos
