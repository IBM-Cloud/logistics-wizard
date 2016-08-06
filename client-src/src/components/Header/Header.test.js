import test from 'ava';
import React from 'react';
import { shallow } from 'enzyme';
import { Header } from './Header';
// import classes from './Header.scss';

const wrapper = shallow(<Header dispatch={() => {}} currentPath="/test" />);

test.todo('make sure correct props are passed into subcomponents');
test.todo('check to see if we can import css modules and assert them in tests');

test('contains an AppBar component', t => {
  t.is(wrapper.find('AppBar').length, 1);
});

test('contains Tabs for navigation', t => {
  t.is(wrapper.find('Tabs').length, 1);
  t.is(wrapper.find('Tab').length, 2);
});
