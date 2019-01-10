const hname = window.location.hostname
export const API = "http://" + hname + ":5000"

const photoAPI = {
  get() {
    return fetch(API + '/images', {})
    .then(statusHelper)
    .then(data => {
      return data
    })
    .catch( (error) => {
      console.log("catch error: " , error)
      return error
    })
  },
}

// thanks: https://github.com/redux-saga/redux-saga/issues/561
function statusHelper (response) {
  let json = response.json(); // there's always a body.
  if (response.status >= 200 && response.status < 300) {
    return json.then(Promise.resolve(response))
  } else {
    if (! json.error) {
      json.error = "Unable to get server settings."
    }
    return json.then(Promise.reject.bind(Promise))
  }
}

export default photoAPI
