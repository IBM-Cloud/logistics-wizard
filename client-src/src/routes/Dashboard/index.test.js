import test from 'ava';
import DashboardRoute from './';

test('(Route) should return a route config object', t => {
  t.is(typeof (DashboardRoute({})), 'object');
});

test('(Route) Config should contain path "dashboard/:guid"', t => {
  t.is(DashboardRoute({}).path, 'dashboard/:guid');
});
