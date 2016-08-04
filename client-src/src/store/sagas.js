import { fork } from 'redux-saga/effects';

export const makeRootSaga = (sagas) => function *rootSaga() {
  yield sagas.map(saga => fork(saga));
};

export const injectSagas = (store, { key, sagas }) => {
  if (store.asyncSagas[key]) {
    return;
  }
  store.asyncSagas[key] = sagas; //eslint-disable-line
  store.runSaga(makeRootSaga(sagas));
};

export default makeRootSaga;
