import test from 'ava';
import React from 'react';
import sinon from 'sinon';
import { bindActionCreators } from 'redux';
import { shallow } from 'enzyme';
import Dashboard from './Dashboard';

const setup = () => {
  const spies = {
    getAdminData: sinon.spy(),
    dispatch: sinon.spy(),
  };
  const props = {
    demoName: 'Test Demo',
    dbdata: { fakeData: 'fake stuff' },
    params: { guid: '1234' },
    ...bindActionCreators({
      getAdminData: spies.getAdminData,
    }, spies.dispatch),
  };
  const component = shallow(<Dashboard {...props} />);

  return { spies, props, component };
};

test.todo('write tests for dashboard elements once complete.');
test('(Component) Renders with expected elements', t => {
  const { props, component } = setup();

  t.true(component.is('div'),
    'is wrapped by a div');
  t.regex(component.find('p').first().text(), new RegExp(props.demoName, 'g'),
    'renders demo name from props');
});

test('(Component) Works as expected.', t => {
  const { spies } = setup();

  t.true(spies.getAdminData.calledOnce,
    'getAdminData is called on creation');
  t.true(spies.dispatch.calledOnce);
});
