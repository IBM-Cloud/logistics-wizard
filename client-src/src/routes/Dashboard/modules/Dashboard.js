// import { delay } from 'redux-saga';
// import { call, take, put, select } from 'redux-saga/effects';

// ------------------------------------
// Constants
// ------------------------------------
export const ADMIN_DATA_RECEIVED = 'Dashboard/ADMIN_DATA_RECEIVED';

// ------------------------------------
// Actions
// ------------------------------------
export const adminDataReceived = (value) => ({
  type: ADMIN_DATA_RECEIVED,
  payload: value,
});

export const actions = {
  adminDataReceived,
};

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  [ADMIN_DATA_RECEIVED]: (state, action) => ({
    ...state,
    ...action.payload,
  }),
};

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
};
export const dashboardReducer = (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type];

  return handler ? handler(state, action) : state;
};
export default dashboardReducer;

// ------------------------------------
// Sagas
// ------------------------------------

// This is set up in `../index.js` as the key in  `injectSagas(store, { key: 'dashboard', sagas });`
export const dashboardSelector = state => state.dashboard;

export const sagas = [
];
