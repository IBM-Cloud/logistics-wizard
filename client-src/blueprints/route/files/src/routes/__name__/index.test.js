import test from 'ava';
import <%= pascalEntityName %>Route from './';

test('(Route) should return a route config object', t => {
  t.is(typeof (<%= pascalEntityName %>Route({})), 'object');
});

test('(Route) Config should contain path "<%= dashesEntityName %>"', t => {
  t.is(<%= pascalEntityName %>Route({}).path, '<%= dashesEntityName %>');
});
