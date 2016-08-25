import test from 'ava';
// import nock from 'nock';
import { reducerTest, actionTest } from 'redux-ava';
import { call, take, select, put } from 'redux-saga/effects';
import {
  CREATE_DEMO,
  CREATE_DEMO_FAILURE,
  createDemo,
  createDemoFailure,
  createDemoReducer,
  createDemoSelector,
  watchCreateDemo,
} from './CreateDemo';
import { receiveDemoSuccess, demoSelector } from 'modules/demos';
import { push } from 'react-router-redux';
import api from 'services';

test('(Constant) CREATE_DEMO === "CreateDemo/CREATE_DEMO"', t => {
  t.is(CREATE_DEMO, 'CreateDemo/CREATE_DEMO');
});

test('(Constant) CREATE_DEMO_FAILURE === "CreateDemo/CREATE_DEMO_FAILURE"', t => {
  t.is(CREATE_DEMO_FAILURE, 'CreateDemo/CREATE_DEMO_FAILURE');
});

test('(Action) createDemo',
  actionTest(
    createDemo,
    { name: 'test' },
    { type: CREATE_DEMO, payload: { name: 'test' } })
  );

test('(Action) createDemoFailure',
  actionTest(
    createDemoFailure,
    { message: 'bad email' },
    { type: CREATE_DEMO_FAILURE, payload: { message: 'bad email' } })
  );

test('(Reducer) initializes with empty state', t => {
  t.deepEqual(createDemoReducer(undefined, {}), {});
});

const testState = () => ({ title: 'A Title', quote: 'A Quote' });

test('(Reducer) return previous state when no action is matched', reducerTest(
  createDemoReducer,
  testState(),
  { type: '@@@@@@@' },
  testState()
));

test('(Reducer) doesnt try to handle saga', reducerTest(
  createDemoReducer,
  testState(),
  createDemo,
  testState(),
));

test('(Saga) watchCreateDemo - API Success', t => {
  const saga = watchCreateDemo();
  const payload = { name: 'test demo', email: 'name@email.com' };
  const createDemoAction = createDemo(payload);
  const demoSession = { mockResponse: 'blah blah' };
  const demoState = { guid: 1234 };

  t.deepEqual(saga.next().value, take(CREATE_DEMO),
    'listens for CREATE_DEMO action.');
  t.deepEqual(saga.next(createDemoAction).value, call(api.createDemo, payload.name, payload.email),
    'calls api with action payload as params.');
  t.deepEqual(saga.next(demoSession).value, put(receiveDemoSuccess(demoSession)),
    'dispatches receiveDemoSuccess action.');
  t.deepEqual(saga.next().value, select(demoSelector),
    'gets the updated state.');
  t.deepEqual(saga.next(demoState).value, put(push(`/dashboard/${demoState.guid}`)),
    'dispatches route change to dashboard');
  t.deepEqual(saga.next().value, take(CREATE_DEMO),
    'saga resets, and begins listening for CREATE_DEMO again.');
});

test.todo('Build a meaningful action around api failure.');
test('(Saga) watchCreateDemo - API Failure', t => {
  const saga = watchCreateDemo();
  const payload = { name: 'test demo', email: 'name@email.com' };
  const createDemoAction = createDemo(payload);
  const error = { message: 'bad email' };

  t.deepEqual(saga.next().value, take(CREATE_DEMO),
    'listens for CREATE_DEMO action.');
  t.deepEqual(saga.next(createDemoAction).value, call(api.createDemo, payload.name, payload.email),
    'calls api with action payload as params.');
  t.deepEqual(saga.throw(error).value, put(createDemoFailure(error)),
    'dispatches createDemoFailure if api call fails.');
  t.deepEqual(saga.next().value, take(CREATE_DEMO),
    'saga resets, and begins listening for CREATE_DEMO again.');
});
