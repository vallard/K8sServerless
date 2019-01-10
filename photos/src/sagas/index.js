import { put, all, call, takeEvery } from 'redux-saga/effects'
import * as actions from '../actions'
import photoAPI from '../services/photos'


export function* get_photos() {
  /* get the photos */
  let response = yield call(photoAPI.get)
  if (response instanceof Error) {
    return yield put(actions.gotError(response))
  }
  console.log(response)
  return yield put(actions.gotPhotos(response.photos))
} 

export function* up_photo(action) {
  /* upload the photo */
  let response = yield call(photoAPI.up, action.data) 
  if (response instanceof Error) {
    return yield put(actions.gotError(response))
  }
  console.log(response)
  return yield put(actions.gotPhotos(response.photos))
}

export function* del_photo(action) {
  /* delete the photo */
  let response = yield call(photoAPI.del, { id : action.id })
  if (response instanceof Error) {
    return yield put(actions.gotError(response))
  }
  console.log(response)
  return yield put(actions.gotPhotos(response.photos))
}
  

export function* watchPhotosRequest() {
  yield takeEvery(actions.GET_PHOTOS, get_photos)
  yield takeEvery(actions.DEL_PHOTO, del_photo)
  yield takeEvery(actions.UP_PHOTO, up_photo)
}


export default function* rootSaga() {
  yield all([
    watchPhotosRequest(),
  ])
}
