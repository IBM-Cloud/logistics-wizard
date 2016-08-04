/* eslint-disable no-unused-expressions */

import React from 'react';
import { shallow } from 'enzyme';
import AppBar from 'material-ui/AppBar';
import { Tabs, Tab } from 'material-ui/Tabs';
import { Header } from './Header';
import classes from './Header.scss';

describe('(Component) Header', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallow(<Header />);
  });

  it('Contains an AppBar component', () => {
    const appbar = wrapper.contains(
      <AppBar />
    );
    expect(appbar).to.exist;
  });

  it('Contains Tabs for navigation', () => {
    const tabs = wrapper.contains(
      <Tabs />
    );
    expect(tabs).to.exist;
    // const tab = tabs.contains(
    //   <Tab label="Styles" value="/styles" />
    // );
    // expect(tab).to.exist;
  });
});
