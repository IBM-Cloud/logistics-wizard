import test from 'ava';
import React from 'react';
import { shallow } from 'enzyme';
import CoreLayout from './CoreLayout';

const child = <h1 className="child">Child</h1>;
const props = {
  children: child,
};
const wrapper = shallow(<CoreLayout {...props} />);

test('should render nested containers', t => {
  t.is(wrapper.find('div').length, 2);
  t.is(wrapper.find('GlobalNav').length, 1);
});

test('children render inside mainContainer div', t => {
  t.truthy(wrapper.find('div').at(1).contains(child));
});

test('containers should use appropriate classes', t => {
  t.truthy(wrapper.find('div').at(0).hasClass('layoutContainer'));
  t.truthy(wrapper.find('div').at(1).hasClass('mainContainer'));
});
