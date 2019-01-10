export const GOT_PHOTOS = 'GOT PHOTOS'
export const GET_PHOTOS = 'GETTING PHOTOS'
export const DEL_PHOTO = 'DEL_PHOTO'
export const UP_PHOTO = 'UPLOAD_PHOTO'
export const ERROR = 'ERROR'

export const gotError = (error) => ({
  type: ERROR,
  error
})

export const gotPhotos = (photos) => ({
  type: GOT_PHOTOS, 
  photos
})

export const getPhotos = () => ({
  type: GET_PHOTOS,
})


export const delPhoto = (photo) => ({
  type: DEL_PHOTO,
  id: photo
})

export const upPhoto = (data) => ({
  type: UP_PHOTO,
  data: data
})
