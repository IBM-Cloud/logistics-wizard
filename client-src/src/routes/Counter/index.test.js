import test from 'ava';
import CounterRoute from './';

test('Should return a route configuration object', t => {
  t.is(typeof (CounterRoute({})), 'object');
});

test('Configuration should contain path `counter`', t => {
  t.is(CounterRoute({}).path, 'counter');
});
