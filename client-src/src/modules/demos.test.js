import test from 'ava';
import { reducerTest, actionTest } from 'redux-ava';
import {
  RECEIVE_DEMO_SUCCESS,
  LOGIN_SUCCESS,
  receiveDemoSuccess,
  loginSuccess,
  demosReducer,
  demoSelector,
} from './demos';

test('(Selector) returns the slice of state for demos.', t => {
  t.deepEqual(demoSelector({ demoSession: { id: '123' } }), { id: '123' });
});

test('(Constant) RECEIVE_DEMO_SUCCESS === "demos/RECEIVE_DEMO_SUCCESS"', t => {
  t.is(RECEIVE_DEMO_SUCCESS, 'demos/RECEIVE_DEMO_SUCCESS');
});

test('(Constant) LOGIN_SUCCESS === "demos/LOGIN_SUCCESS"', t => {
  t.is(LOGIN_SUCCESS, 'demos/LOGIN_SUCCESS');
});

test('(Action) receiveDemoSuccess',
  actionTest(
    receiveDemoSuccess,
    { name: 'test' },
    { type: RECEIVE_DEMO_SUCCESS, payload: { name: 'test' } })
  );

test('(Action) loginSuccess',
  actionTest(
    loginSuccess,
    { name: 'test' },
    { type: LOGIN_SUCCESS, payload: { name: 'test' } })
  );

test('(Reducer) initializes with empty state', t => {
  t.deepEqual(demosReducer(undefined, {}), {});
});

test('(Reducer) return previous state when no action is matched', reducerTest(
  demosReducer,
  {},
  { type: '@@@@@@@' },
  {},
));

test('(Reducer) stores token on loginSuccess', reducerTest(
  demosReducer,
  {},
  loginSuccess('login-token'),
  { token: 'login-token' },
));

const demoApiResponse = () => ({
  name: 'demo',
  guid: 'guid',
  id: 'id',
  users: [{
    username: 'johndoe',
    roles: [{ name: 'Supply Chain Manager' }],
  }],
});

test('(Reducer) adds demo session to state on receiveDemoSuccess', reducerTest(
  demosReducer,
  {},
  receiveDemoSuccess(demoApiResponse()),
  {
    name: 'demo',
    guid: 'guid',
    id: 'id',
    roles: [{
      username: 'johndoe',
      type: 'Supply Chain Manager',
    }],
  },
));
