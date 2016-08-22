import test from 'ava';
import ExampleRoute from './';

test('(Route) should return a route config object', t => {
  t.is(typeof (ExampleRoute({})), 'object');
});

test('(Route) Config should contain path "example"', t => {
  t.is(ExampleRoute({}).path, 'example');
});
