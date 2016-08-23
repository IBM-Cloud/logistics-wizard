import { call, take, put, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import api from 'services';

import { loginSuccess, receiveDemoSession, demoSelector } from 'modules/demos';
import { adminDataReceived } from 'routes/Dashboard/modules/Dashboard';

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

export function *watchCreateDemo() {
  while (true) {
    const { payload } = yield take(CREATE_DEMO);
    try {
      const demoSession = yield call(api.createDemo, payload.name, payload.email);
      yield put(receiveDemoSession(demoSession));
      const demoState = yield select(demoSelector);
      yield put(push(`/dashboard/${demoState.guid}`));
      const token = yield call(api.login, demoState.id, demoState.guid);
      yield put(loginSuccess(token));
      const adminData = yield call(api.getAdminData, token.token);
      yield put(adminDataReceived(adminData));
    }
    catch (error) {
      console.log(error);
    }
  }
}

export const sagas = [
  watchCreateDemo,
];
