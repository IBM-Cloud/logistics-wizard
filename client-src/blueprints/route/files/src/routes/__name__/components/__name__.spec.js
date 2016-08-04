/* eslint-disable no-unused-expressions */

import React from 'react';
import { bindActionCreators } from 'redux';
import { shallow } from 'enzyme';
import { <%= pascalEntityName %> } from './<%= pascalEntityName %>';
import classes from './<%= pascalEntityName %>.scss';

describe('(Component) <%= pascalEntityName %>', () => {
  let props;
  let spies;
  let wrapper;

  beforeEach(() => {
    spies = {};
    props = {
      title: 'This is a fake prop for testing',
      ...bindActionCreators({
        coolAction: (spies.coolAction = sinon.spy()),
      }, spies.dispatch = sinon.spy()),
    };
    wrapper = shallow(<<%= pascalEntityName %> {...props} />);
  });

  it('Should render as a <div>.', () => {
    expect(wrapper.is('div')).to.equal(true);
  });

  it('uses css module in wrapper div', () => {
    expect(wrapper.hasClass(classes.<%= pascalEntityName %>)).to.be.true;
  });

  it('Should render with an <h4> that includes Component name and title prop.', () => {
    expect(wrapper.find('h4').text()).to.match(/<%= pascalEntityName %> - This is a fake prop for testing/);
  });

  describe('A basic button...', () => {
    let button;

    beforeEach(() => {
      button = wrapper.find('button').filterWhere(a => a.text() === 'Click Me!');
    });

    it('Should dispatch a `cool` action when clicked', () => {
      spies.dispatch.should.have.not.been.called;

      button.simulate('click');

      spies.dispatch.should.have.been.called;
      spies.coolAction.should.have.been.called;
    });
  });
});
