import { put, all, takeEvery } from 'redux-saga/effects'
import * as actions from '../actions'


export function* get_photos() {
  return yield put(actions.gotPhotos(""))
} 

export function* watchPhotosRequest() {
  yield takeEvery(actions.GET_PHOTOS, get_photos)
}

export default function* rootSaga() {
  yield all([
    watchPhotosRequest(),
  ])
}
