import test from 'ava';
import { delay } from 'redux-saga';
import { call, put, take, select } from 'redux-saga/effects';
import { reducerTest, actionTest } from 'redux-ava';
import fromGenerator from 'redux-saga-test';
import {
  COUNTER_INCREMENT,
  COUNTER_DOUBLE,
  increment,
  double,
  doubleAsync,
  default as counterReducer,
} from './counter';

test('(Constant) COUNTER_INCREMENT === "COUNTER_INCREMENT".', t => {
  t.is(COUNTER_INCREMENT, 'COUNTER_INCREMENT');
});

test('(Constant) COUNTER_DOUBLE === "COUNTER_DOUBLE".', t => {
  t.is(COUNTER_DOUBLE, 'COUNTER_DOUBLE');
});

test('(Action) increment: Should set payload to first argument',
  actionTest(increment, 5, { type: COUNTER_INCREMENT, payload: 5 })
);

test('(Action) increment: removes decimals',
  actionTest(increment, 5.5, { type: COUNTER_INCREMENT, payload: 5 })
);

test('(Action) increment: Should set payload to 1 if nothing is provided',
  actionTest(increment, undefined, { type: COUNTER_INCREMENT, payload: 1 })
);

test('(Action) increment: handles invalid payload',
  actionTest(increment, '@@@', { type: COUNTER_INCREMENT, payload: 1 })
);

test('(Action) double: return type "COUNTER_DOUBLE"',
  actionTest(double, null, { type: COUNTER_DOUBLE })
);

test('(Reducer) Should initialize with a state of 0 (Number).', t => {
  t.is(counterReducer(undefined, {}), 0);
});

test('(Reducer) increments the state.', reducerTest(
  counterReducer,
  0,
  increment(5),
  5
));

test('(Reducer) returns previous state if action is not matched.', reducerTest(
  counterReducer,
  5,
  { type: '@@@@@@' },
  5
));

test('(Saga) doubleAsync: Double the value of the current state.', t => {
  const state = { counter: 5 };
  const generator = doubleAsync();
  const saga = fromGenerator(t, doubleAsync());

  // saga.next().take(COUNTER_DOUBLE);
  // saga.next().select();
  // saga.next(state).call(delay, 200);
  // saga.next().put(increment(state.counter));
  // saga.next().take(COUNTER_DOUBLE);

  t.deepEqual(generator.next().value, take(COUNTER_DOUBLE),
    'listens for COUNTER_DOUBLE action.');

  t.deepEqual(generator.next().value, select(),
    'selects the current state');

  t.deepEqual(generator.next(state).value, call(delay, 200),
    'delays to simulate an async call');

  t.deepEqual(generator.next().value, put(increment(state.counter)),
    'increments by current counter amount.');

  t.deepEqual(generator.next().value, take(COUNTER_DOUBLE),
    'the loop continues');
});
