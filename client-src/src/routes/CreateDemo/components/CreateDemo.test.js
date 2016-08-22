import test from 'ava';
import React from 'react';
import sinon from 'sinon';
import { bindActionCreators } from 'redux';
import { shallow } from 'enzyme';
import { CreateDemo } from './CreateDemo';

const setup = (quote) => {
  const spies = {
    createDemo: sinon.spy(),
    dispatch: sinon.spy(),
  };
  const props = {
    containerQuery: { full: true },
    quote,
    ...bindActionCreators({
      createDemo: spies.createDemo,
    }, spies.dispatch),
  };
  const component = shallow(<CreateDemo {...props} />);

  return { spies, props, component };
};

test.todo('Write tests for CreateDemo Component elements');
test('(Component) Renders with expected elements', t => {
  // const { props, component } = setup();
  t.pass();
});

test('(Component) Works as expected.', t => {
  const { spies, component } = setup();

  t.false(spies.createDemo.calledOnce);
  t.false(spies.dispatch.calledOnce);
  component.find('RaisedButton').first().simulate('click');
  t.true(spies.dispatch.calledOnce);
  t.true(spies.createDemo.calledOnce,
    'calls createDemo when clicked');
});
