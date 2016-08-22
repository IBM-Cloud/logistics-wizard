import test from 'ava';

test.todo('(Duck) write tests for Dashboard.');
/*
import nock from 'nock';
import { reducerTest, actionTest } from 'redux-ava';
import { delay } from 'redux-saga';
import { call, take, select, put } from 'redux-saga/effects';
import {
  UPDATE_TITLE,
  GET_QUOTE,
  RECEIVE_QUOTE,
  updateTitle,
  getQuote,
  receiveQuote,
  dashboardReducer,
  dashboardSelector,
  fetchQuote, // This would normally come from an api caller module
  watchGetQuote,
} from './Dashboard';

// This test would not normally be here, but the fetch api is included for this example to work.
test('(API) fetchQuote', t => {
  const apiUrl = 'http://quotes.rest';
  const endpoint = '/qod.json?category=inspire';
  const reply = {
    contents: {
      quotes: [{
        quote: 'Quote of the day.',
      }],
    },
  };

  nock(apiUrl)
    .get(endpoint)
    .reply(200, reply);
  return fetchQuote().then(response => {
    t.deepEqual(response, reply.contents.quotes[0].quote);
  });
});

test('(Constant) UPDATE_TITLE === "Dashboard/UPDATE_TITLE"', t => {
  t.is(UPDATE_TITLE, 'Dashboard/UPDATE_TITLE');
});

test('(Constant) GET_QUOTE === "Dashboard/GET_QUOTE"', t => {
  t.is(GET_QUOTE, 'Dashboard/GET_QUOTE');
});

test('(Constant) RECEIVE_QUOTE === "Dashboard/RECEIVE_QUOTE"', t => {
  t.is(RECEIVE_QUOTE, 'Dashboard/RECEIVE_QUOTE');
});

test('(Action) updateTitle',
  actionTest(updateTitle, 'title text', { type: UPDATE_TITLE, payload: 'title text' }));

test('(Action) getQuote',
  actionTest(getQuote, undefined, { type: GET_QUOTE }));

test('(Action) receiveQuote',
  actionTest(receiveQuote, 'quote text', { type: RECEIVE_QUOTE, payload: 'quote text' }));

test('(Reducer) initializes with title state', t => {
  t.deepEqual(dashboardReducer(undefined, {}), { title: 'A Title Stored in global state.' });
});

const testState = () => ({ title: 'A Title', quote: 'A Quote' });

test('(Reducer) return previous state when no action is matched', reducerTest(
  dashboardReducer,
  testState(),
  { type: '@@@@@@@' },
  testState()
));

test('(Reducer) doesnt try to handle saga', reducerTest(
  dashboardReducer,
  testState(),
  getQuote,
  testState(),
));

test('(Reducer) updates title', reducerTest(
  dashboardReducer,
  testState(),
  updateTitle('New Title'),
  { title: 'New Title', quote: 'A Quote' }
));

test('(Reducer) updates quote', reducerTest(
  dashboardReducer,
  testState(),
  receiveQuote('New Quote'),
  { title: 'A Title', quote: 'New Quote' }
));

test('(Saga) watchGetQuote: no quote received.', t => {
  const saga = watchGetQuote();
  const state = {
    title: 'Initial Title',
  };
  const mockQuote = 'A Very Insightful Quote.';

  t.deepEqual(saga.next().value, take(GET_QUOTE),
    'listens for GET_QUOTE action.');

  t.deepEqual(saga.next().value, select(dashboardSelector),
    'grabs the current state.');

  t.deepEqual(saga.next(state).value, put(updateTitle('You dispatched an action!')),
    'updates title.');

  t.deepEqual(saga.next().value, put(receiveQuote('Fetching Quote...')),
    'quote message updates with fetching message.');

  t.deepEqual(saga.next().value, call(fetchQuote),
    'calls fetchQuote api.');

  t.deepEqual(saga.next(mockQuote).value, call(delay, 1000),
    'simulates long load time by calling delay.');

  t.deepEqual(saga.next().value, put(receiveQuote(mockQuote)),
    'updates quote in state with quote received from api.');

  t.deepEqual(saga.next().value, take(GET_QUOTE),
    'loops back to listening for GET_QUOTE action.');
});

test('(Saga) watchGetQuote: quote already received.', t => {
  const saga = watchGetQuote();
  const state = {
    title: 'You dispatched an action!',
    quote: 'Insightful quote of the day',
  };

  t.deepEqual(saga.next().value, take(GET_QUOTE),
    'listens for GET_QUOTE action.');

  t.deepEqual(saga.next().value, select(dashboardSelector),
    'grabs the current state.');

  t.deepEqual(saga.next(state).value, put(updateTitle('You already have a quote.')),
    'grabs the current state.');

  t.deepEqual(saga.next().value, take(GET_QUOTE),
    'loops back to listening for GET_QUOTE action.');
});

*/
