/* eslint-disable no-unused-expressions */

import React from 'react';
import { render } from 'enzyme';
import { HomeView } from './HomeView';

describe('(View) Home', () => {
  let component;

  beforeEach(() => {
    component = render(<HomeView />);
  });

  it('Renders a welcome message', () => {
    const welcome = component.find('h4');
    expect(welcome).to.exist;
    expect(welcome.text()).to.match(/Welcome!/);
  });

  it('Renders an awesome duck image', () => {
    const duck = component.find('img');
    expect(duck).to.exist;
    expect(duck.attr('alt')).to.match(/This is a duck, because Redux!/);
  });
});
