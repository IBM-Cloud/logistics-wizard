import test from 'ava';
import CreateDemoRoute from './';

test('(Route) should return a route config object', t => {
  t.is(typeof (CreateDemoRoute({})), 'object');
});

test('(Route) Config should contain path "create-demo"', t => {
  t.is(CreateDemoRoute({}).path, 'create-demo');
});
