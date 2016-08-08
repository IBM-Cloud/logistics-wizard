import test from 'ava';
import React from 'react';
import sinon from 'sinon';
import { bindActionCreators } from 'redux';
import { shallow } from 'enzyme';
import { <%= pascalEntityName %> } from './<%= pascalEntityName %>';

const setup = (quote) => {
  const spies = {
    actionAndSaga: sinon.spy(),
    dispatch: sinon.spy(),
  };
  const props = {
    title: 'Title',
    quote,
    ...bindActionCreators({
      actionAndSaga: spies.actionAndSaga,
    }, spies.dispatch),
  };
  const component = shallow(<<%= pascalEntityName %> {...props} />);

  return { spies, props, component };
};

test('(Component) Renders with expected elements', t => {
  const { props, component } = setup();

  t.true(component.is('div'),
    'is wrapped by a div');
  t.true(component.hasClass('<%= camelEntityName %>'),
    'uses class "<%= camelEntityName %>" in wrapper div');
  t.is(component.find('h4').length, 2,
    'has two h4 elements');
  t.is(component.find('h4').first().text(), `<%= pascalEntityName %> - ${props.title}`,
    'title is ComponentName - props.title');
  t.is(component.find('button').length, 1,
    'has 1 button');
  t.is(component.find('button').first().text(), 'Click Me!',
    'button has click me text');
  t.is(component.find('h4').last().text(), 'Click button to receive a quote.',
    '2nd h4 has default quote message');
});

test('(Component) Renders quote if there is one', t => {
  const { props, component } = setup('Quote');

  t.is(component.find('h4').last().text(), props.quote,
    '2nd h4 displays quote');
});

test('(Component) Works as expected.', t => {
  const { spies, component } = setup();

  t.false(spies.actionAndSaga.calledOnce);
  t.false(spies.dispatch.calledOnce);
  component.find('button').first().simulate('click');
  t.true(spies.dispatch.calledOnce);
  t.true(spies.actionAndSaga.calledOnce,
    'calls actionAndSaga when clicked');
});
