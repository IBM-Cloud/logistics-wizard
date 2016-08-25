import test from 'ava';
import CreateDemoRoute from './';

test('(Route) returns a route config object', t => {
  t.is(typeof (CreateDemoRoute({})), 'object');
});

test('(Route) has path "create-demo"', t => {
  t.is(CreateDemoRoute({}).path, 'create-demo');
});
