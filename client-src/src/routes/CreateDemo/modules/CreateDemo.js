import { call, take, put, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';

// ------------------------------------
// Constants
// ------------------------------------
export const CREATE_DEMO = 'CreateDemo/CREATE_DEMO';

// ------------------------------------
// Actions
// ------------------------------------
export const createDemo = () => ({
  type: CREATE_DEMO,
});

export const actions = {
  createDemo,
};

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  // [UPDATE_TITLE]: (state, action) => ({
  //   ...state,
  //   title: action.payload,
  // }),
  // [RECEIVE_QUOTE]: (state, action) => ({
  //   ...state,
  //   quote: action.payload,
  // }),
};

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = { };
export const createDemoReducer = (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type];

  return handler ? handler(state, action) : state;
};
export default createDemoReducer;

// ------------------------------------
// Sagas
// ------------------------------------

// This is set up in `../index.js` as the key in  `injectSagas(store, { key: 'createDemo', sagas });`
export const createDemoSelector = state => state.createDemo;

export function *watchCreateDemo() {
  while (true) {
    yield take(CREATE_DEMO);
    // const state = yield select(createDemoSelector);
    console.log('Creating Demo');
    yield put(push('/dashboard'));
  }
}

export const sagas = [
  watchCreateDemo,
];
