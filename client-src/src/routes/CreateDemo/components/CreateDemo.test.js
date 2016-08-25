import test from 'ava';
import React from 'react';
import sinon from 'sinon';
import { bindActionCreators } from 'redux';
import { shallow } from 'enzyme';
import { CreateDemo } from './CreateDemo';

test.todo('Move hard coded colors in sass file to reference a colors theme object.');
test.todo('Add error state/response from failed createDemo call.');

const setup = (full = true) => {
  const spies = {
    createDemo: sinon.spy(),
    dispatch: sinon.spy(),
  };
  const props = {
    containerQuery: { full },
    ...bindActionCreators({
      createDemo: spies.createDemo,
    }, spies.dispatch),
  };
  const component = shallow(<CreateDemo {...props} />);

  return { spies, props, component };
};

test('(Component) Renders with needed elements for interaction', t => {
  const { component } = setup();
  t.is(component.find('TextField').length, 2,
    'Has two inputs for name/email');
  t.is(component.find('TextField').first().props().id, 'demoName');
  t.is(component.find('TextField').last().props().id, 'email');
  t.is(component.find('RaisedButton').length, 1,
    'has a button to create a demo');
  t.is(typeof (component.find('RaisedButton').first().prop('onClick')), 'function',
    'uses onClick prop to call a function');
});

test('(Component) is responsive.', t => {
  let { component } = setup(false);
  t.false(component.find('div').first().hasClass('full'));

  component = setup().component;
  t.true(component.find('div').first().hasClass('full'));
});

test('(Component) Create Demo button works as expected.', t => {
  const { spies, component } = setup();

  t.false(spies.createDemo.calledOnce);
  t.false(spies.dispatch.calledOnce);

  const nameField = component.find('TextField').first();
  nameField.simulate('change', { target: { id: 'demoName', value: 'test text' } });
  component.find('RaisedButton').first().simulate('click');
  t.true(spies.dispatch.calledOnce);
  t.true(spies.createDemo.calledOnce,
    'calls createDemo when clicked');
  t.deepEqual(spies.createDemo.args[0][0], { name: 'test text' },
    'passes name value from text field to createDemo');

  nameField.simulate('change', { target: { id: 'email', value: 'email@company.com' } });
  component.find('RaisedButton').first().simulate('click');
  t.deepEqual(spies.createDemo.args[1][0], { name: 'test text', email: 'email@company.com' },
    'if email is entered, it is also passed');
});
