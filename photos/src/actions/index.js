export const GOT_PHOTOS = 'GOT PHOTOS'
export const GET_PHOTOS = 'GETTING PHOTOS'
export const ERROR = 'ERROR'

export const gotPhotos = (photos) => ({
  type: GOT_PHOTOS, 
  photos
})

export const getPhotos = () => ({
  type: GET_PHOTOS,
})

export const gotError = (error) => ({
  type: ERROR,
  error
})
