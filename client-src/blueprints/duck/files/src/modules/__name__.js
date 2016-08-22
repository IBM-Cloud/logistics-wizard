// NOTE: This will need to be hooked up to 'store/reducers' and 'store/sagas'

import { delay } from 'redux-saga';
import { call, take, put, select } from 'redux-saga/effects';
// ------------------------------------
// Constants
// ------------------------------------
export const UPDATE_NAME = '<%= camelEntityName %>/UPDATE_NAME';
export const TOGGLE_MENU = '<%= camelEntityName %>/TOGGLE_MENU';
export const START_SAGA = '<%= camelEntityName %>/START_SAGA';

// ------------------------------------
// Actions
// ------------------------------------
export const updateName = (value) => ({
  type: UPDATE_NAME,
  payload: value,
});

export const toggle = () => ({
  type: TOGGLE_MENU,
});

export const startSaga = () => ({
  type: START_SAGA,
});

export const actions = {
  updateName,
  toggle,
  startSaga,
};

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  [UPDATE_NAME]: (state, action) => ({
    ...state,
    name: action.payload,
  }),
  [TOGGLE_MENU]: (state) => ({
    ...state,
    toggled: !state.toggled,
  }),
};

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  name: 'Enter your name',
  toggled: false,
};
export const <%= camelEntityName %>Reducer = (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type];

  return handler ? handler(state, action) : state;
};
export default <%= camelEntityName %>Reducer;

// ------------------------------------
// Sagas
// ------------------------------------

export function *beginSaga() {
  while (true) {
    yield take(START_SAGA);
    console.log('<%= camelEntityName %>: Beginning Saga');
    // const state = yield select(); // grab the state
    yield call(delay, 1000); // Simulate an async call
    yield put(actions.toggle());
    console.log('<%= camelEntityName %>: Saga Complete, dispatching toggle');
  }
}

export const sagas = [
  beginSaga,
];
