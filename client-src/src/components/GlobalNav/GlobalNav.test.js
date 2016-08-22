import test from 'ava';
import sinon from 'sinon';
import React from 'react';
import { shallow } from 'enzyme';
import GlobalNav from './GlobalNav';

const setup = () => {
  const spies = {
    clicky: sinon.spy(),
  };
  const props = {
    customProp: 'Test',
    clicky: spies.clicky,
  };
  const component = shallow(<GlobalNav {...props} />);

  return { spies, props, component };
};

test('(Component) Has expected elements.', t => {
  const { props, component } = setup();

  t.true(component.is('div'),
    'is wrapped by a div.');
  t.true(component.hasClass('globalNav'),
    'wrapper uses proper class.');
});
