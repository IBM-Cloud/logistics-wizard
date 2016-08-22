import test from 'ava';
import sinon from 'sinon';
import React from 'react';
import { shallow } from 'enzyme';
import { bindActionCreators } from 'redux';
import { Counter } from './Counter';

const setup = () => {
  const spies = {
    doubleAsync: sinon.spy(),
    increment: sinon.spy(),
    dispatch: sinon.spy(),
  };
  const props = {
    counter: 5,
    ...bindActionCreators({
      doubleAsync: spies.doubleAsync,
      increment: spies.increment,
    }, spies.dispatch),
  };
  const component = shallow(<Counter {...props} />);

  return { spies, props, component };
};

test('Should render as a <div>.', t => {
  t.true(setup().component.is('div'));
});

test('Should render with an <h2> that includes Sample Counter text.', t => {
  const { component } = setup();

  t.regex(component.find('h2').text(), /Counter:/);
});

test('Should render props.counter at the end of the sample counter <h2>.', t => {
  const { component } = setup();

  t.regex(component.find('h2').text(), /5$/);
  component.setProps({ counter: 8 });
  t.regex(component.find('h2').text(), /8$/);
});

test('Should render exactly two buttons.', t => {
  const { component } = setup();
  const buttons = component.find('RaisedButton');

  t.is(buttons.length, 2);
  t.regex(buttons.first().props().label, /Increment/);
  t.regex(buttons.last().props().label, /Double/);
});

test('Increment button should dispatch an `increment` action when clicked', t => {
  const { spies, component } = setup();
  const button = component.find('RaisedButton').first();

  t.false(spies.dispatch.called);
  button.simulate('click');
  t.true(spies.dispatch.calledOnce);
  t.true(spies.increment.calledOnce);
});

test('Double button should dispatch a `doubleAsync` action when clicked', t => {
  const { spies, component } = setup();
  const button = component.find('RaisedButton').last();

  t.false(spies.dispatch.called);
  button.simulate('click');
  t.true(spies.dispatch.calledOnce);
  t.true(spies.doubleAsync.calledOnce);
});
