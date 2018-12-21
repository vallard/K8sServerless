import React from 'react'
import createSagaMiddleware from 'redux-saga'
import { createLogger } from 'redux-logger'
import { render } from 'react-dom'
import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'
import App from './components/App'
import reducer from './reducers'
import rootSaga from './sagas'

const loggerMiddleware = createLogger()
const sagaMiddleware = createSagaMiddleware()

const store = createStore(
  reducer,
  applyMiddleware(
    sagaMiddleware,
    loggerMiddleware
  )
)

sagaMiddleware.run(rootSaga)

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
)
