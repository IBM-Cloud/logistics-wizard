import { call, take, put, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import api from 'services';

import { loginSuccess, receiveDemoSuccess, demoSelector } from 'modules/demos';
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
      yield put(receiveDemoSuccess(demoSession));
    }
    catch (error) {
      console.log(error);
      // yield put(createDemoFailure(error));
    }

    const demoState = yield select(demoSelector);
    yield put(push(`/dashboard/${demoState.guid}`));
  }
}

export const sagas = [
  watchCreateDemo,
];
