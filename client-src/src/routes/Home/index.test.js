import test from 'ava';
import HomeRoute from './';

test('should return a route config object', t => {
  t.is(typeof (HomeRoute), 'object');
});

test('should define a route component', t => {
  t.is(HomeRoute.component().type, 'div');
});
