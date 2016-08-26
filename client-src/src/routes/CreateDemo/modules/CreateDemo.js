import { call, take, put, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import api from 'services';

import { receiveDemoSuccess, demoSelector } from 'modules/demos';

export const createDemoSelector = state => state.createDemo;
// ------------------------------------
// Constants
// ------------------------------------

export const CREATE_DEMO = 'CreateDemo/CREATE_DEMO';
export const CREATE_DEMO_FAILURE = 'CreateDemo/CREATE_DEMO_FAILURE';

// ------------------------------------
// Actions
// ------------------------------------
export const createDemo = (value) => ({
  type: CREATE_DEMO,
  payload: value,
});

export const createDemoFailure = (value) => ({
  type: CREATE_DEMO_FAILURE,
  payload: value,
});

export const actions = {
  createDemo,
  createDemoFailure,
};

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  [CREATE_DEMO_FAILURE]: (state, action) => {
    console.error(action.payload);

    return {
      ...state,
      error: action.payload.message,
    };
  },
};

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {};
export const createDemoReducer = (state = initialState, action) => {
  const handler = ACTION_HANDLERS[action.type];

  return handler ? handler(state, action) : state;
};
export default createDemoReducer;

// ------------------------------------
// Sagas
// ------------------------------------
export function *watchCreateDemo() {
  while (true) {
    const { payload } = yield take(CREATE_DEMO);

    try {
      const demoSession = yield call(api.createDemo, payload.name, payload.email);
      yield put(receiveDemoSuccess(demoSession));
      const demoState = yield select(demoSelector);
      yield put(push(`/dashboard/${demoState.guid}`));
    }
    catch (error) {
      yield put(createDemoFailure(error));
    }
  }
}

export const sagas = [
  watchCreateDemo,
];
