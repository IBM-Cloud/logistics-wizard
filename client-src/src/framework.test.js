import React from 'react';
import test from 'ava';
import { mount, render, shallow } from 'enzyme';

test('A passing test can run', t => {
  t.pass();
});

test('works with enzyme', t => {
  const Fixture = () => (
    <div>
      <input id="checked" defaultChecked />
      <input id="not" defaultChecked={false} />
    </div>
  );

  let wrapper = shallow(<Fixture />);
  t.is(wrapper.find('input').length, 2);
  t.is(wrapper.find('#checked').props().defaultChecked, true);
  t.is(wrapper.find('#not').props().defaultChecked, false);

  wrapper = mount(<Fixture />);
  t.is(wrapper.find('input').length, 2);
  t.is(wrapper.find('#checked').props().defaultChecked, true);
  t.is(wrapper.find('#not').props().defaultChecked, false);

  wrapper = render(<Fixture />);
  t.is(wrapper.find('input').length, 2);
  t.is(wrapper.find('#checked').attr('checked'), 'checked');
  t.is(wrapper.find('#not').attr('checked'), undefined);
});
