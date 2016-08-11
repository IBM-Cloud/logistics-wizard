import test from 'ava';
import sinon from 'sinon';
import React from 'react';
import { shallow } from 'enzyme';
import <%= pascalEntityName %> from './<%= pascalEntityName %>';

const setup = () => {
  const spies = {
    clicky: sinon.spy(),
  };
  const props = {
    customProp: 'Test',
    clicky: spies.clicky,
  };
  const component = shallow(<<%= pascalEntityName %> {...props} />);

  return { spies, props, component };
};

test('(Component) Has expected elements.', t => {
  const { props, component } = setup();

  t.true(component.is('div'),
    'is wrapped by a div.');
  t.true(component.hasClass('<%= camelEntityName %>'),
    'wrapper uses proper class.');
  t.is(component.find('h1').length, 1,
    'has header');
  t.is(component.find('h1').first().text(), '<%= pascalEntityName %>',
    'header text matches component name');
  t.is(component.find('h2').length, 1,
    'has sub-header');
  t.regex(component.find('h2').first().text(), new RegExp(props.customProp, 'g'),
    'sub-header contains customProp');
  t.is(component.find('button').length, 1,
    'has a button');
  t.is(component.find('button').first().text(), 'Clicky',
    'Button has text: Clicky');
});

test('(Component) Works as expected.', t => {
  const { spies, component } = setup();

  t.false(spies.clicky.calledOnce);
  component.find('button').first().simulate('click');
  t.true(spies.clicky.calledOnce,
    'calls clicky prop when clicked');
});
