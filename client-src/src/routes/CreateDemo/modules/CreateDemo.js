import { call, take, put, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import { createDemoSuccess } from 'modules/demos';

// ------------------------------------
// Constants
// ------------------------------------
export const CREATE_DEMO = 'CreateDemo/CREATE_DEMO';

// ------------------------------------
// Actions
// ------------------------------------
export const createDemo = (value) => ({
  type: CREATE_DEMO,
  payload: value,
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
export const createDemoSelector = state => state.createDemo;

export const apiCreateDemo = (body) => {
  const controllerHost = 'http://dev-logistics-wizard.mybluemix.net/api/v1';
  // const erpHost = 'http://dev-logistics-wizard-erp.mybluemix.net/api/v1';
  const endpoint = '/demos';
  const params = {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(body),
  };

  return fetch(`${controllerHost}${endpoint}`, params)
    .then(response => response.json());
};

export function *watchCreateDemo() {
  while (true) {
    const { payload } = yield take(CREATE_DEMO);
    try {
      const demoSession = yield call(apiCreateDemo, payload);
      yield put(push('/dashboard'));
      yield put(createDemoSuccess(demoSession));
    }
    catch (error) {
      console.log('error:', error);
    }
  }
}

export const sagas = [
  watchCreateDemo,
];
