import test from 'ava';
import React from 'react';
import { shallow } from 'enzyme';
import { HomeView } from './HomeView';

const component = () => shallow(<HomeView />);

test('Renders a welcome message', t => {
  const welcome = component().find('h4');
  t.is(welcome.length, 1);
  t.regex(welcome.text(), /Welcome!/);
});

test('Renders an awesome duck image', t => {
  const image = component().find('img');
  t.is(image.length, 1);
  t.regex(image.props().alt, /This is a duck, because Redux!/);
});
