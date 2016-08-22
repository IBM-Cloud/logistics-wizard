import test from 'ava';
import React from 'react';
import { shallow } from 'enzyme';
import { Icon } from 'react-fa';
import GlobalNav from './GlobalNav';


const setup = () => {
  // const spies = {
  //   clicky: sinon.spy(),
  // };
  // const props = {
  //   customProp: 'Test',
  //   clicky: spies.clicky,
  // };
  const component = shallow(<GlobalNav />);

  return { component };
};

test('(Component) Has expected elements.', t => {
  const { component } = setup();

  // t.is(component.find('Icon'), 1,
  //   'contains React-FA Github Icons.');
  // t.true(component.contains('<RoleSwitcher />'),
  //   'contains RoleSwitcher component.');
  // t.true(component.contains('<Toolbar />'),
  //   'contains Toolbar component.');

  t.is(component.find('Icon').length, 1);
  t.is(component.find('RoleSwitcher').length, 1);
  t.is(component.find('Toolbar').length, 1);
});
