import { put, all, call, takeEvery } from 'redux-saga/effects'
import * as actions from '../actions'
import photoAPI from '../services/photos'


export function* get_photos() {
  let response = yield call(photoAPI.get)
  if (response instanceof Error) {
    return yield put(actions.gotError(response))
  }
  console.log(response)
  return yield put(actions.gotPhotos(response.photos))
} 

export function* watchPhotosRequest() {
  yield takeEvery(actions.GET_PHOTOS, get_photos)
}

export default function* rootSaga() {
  yield all([
    watchPhotosRequest(),
  ])
}
