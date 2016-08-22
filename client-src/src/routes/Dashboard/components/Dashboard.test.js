import test from 'ava';
import React from 'react';
import { bindActionCreators } from 'redux';
import { shallow } from 'enzyme';
import { Dashboard } from './Dashboard';

const setup = () => {
  const spies = {
  };
  const props = {
    demoName: 'Test Demo',
    ...bindActionCreators({
    }, spies.dispatch),
  };
  const component = shallow(<Dashboard {...props} />);

  return { spies, props, component };
};

test.todo('write tests for dashboard elements once complete.');
test('(Component) Renders with expected elements', t => {
  const { component } = setup();

  t.true(component.is('div'),
    'is wrapped by a div');
});
