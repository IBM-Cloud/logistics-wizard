/* eslint-disable no-unused-expressions */

import React from 'react';
import { bindActionCreators } from 'redux';
import { shallow } from 'enzyme';
import { <%= pascalEntityName %> } from './<%= pascalEntityName %>';

describe('(Component) <%= pascalEntityName %>', () => {
  let props;
  let spies;
  let wrapper;

  beforeEach(() => {
    spies = {};
    props = {
      counter: 5,
      ...bindActionCreators({
        doubleAsync: (spies.doubleAsync = sinon.spy()),
        increment: (spies.increment = sinon.spy()),
      }, spies.dispatch = sinon.spy()),
    };
    wrapper = shallow(<<%= pascalEntityName %> {...props} />);
  });

  it('Should render as a <div>.', () => {
    expect(wrapper.is('div')).to.equal(true);
  });

  it('Should render with an <h2> that includes Sample Counter text.', () => {
    expect(wrapper.find('h2').text()).to.match(/Counter:/);
  });

  it('Should render props.counter at the end of the sample counter <h2>.', () => {
    expect(wrapper.find('h2').text()).to.match(/5$/);
    wrapper.setProps({ counter: 8 });
    expect(wrapper.find('h2').text()).to.match(/8$/);
  });

  it('Should render exactly two buttons.', () => {
    expect(wrapper.find('RaisedButton')).to.have.length(2);
  });

  describe('An increment button...', () => {
    let button;

    beforeEach(() => {
      button = wrapper.find('RaisedButton').filterWhere(a => a.props().label === 'Increment');
    });

    it('Should dispatch a `increment` action when clicked', () => {
      spies.dispatch.should.have.not.been.called;

      button.simulate('click');

      spies.dispatch.should.have.been.called;
      spies.increment.should.have.been.called;
    });
  });

  describe('A Double (Async) button...', () => {
    let button;

    beforeEach(() => {
      button = wrapper.find('RaisedButton').filterWhere(a => a.props().label === 'Double (Async)');
    });

    it('Should dispatch a `doubleAsync` action when clicked', () => {
      spies.dispatch.should.have.not.been.called;

      button.simulate('click');

      spies.dispatch.should.have.been.called;
      spies.doubleAsync.should.have.been.called;
    });
  });
});
