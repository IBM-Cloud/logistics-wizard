import React from 'react';
import AppBar from 'material-ui/AppBar';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import { Tabs, Tab } from 'material-ui/Tabs';
import classes from './Header.scss';

const clickTitle = () => (
  <span className={classes.title}>
    Logistics Wizard Demo
  </span>
);

export const Header = (props) => (
  <div>
    <AppBar
      title={clickTitle()}
      onLeftIconButtonTouchTap={props.toggleMenu}
      onTitleTouchTap={() => props.goto('/')}
    />
    <Tabs
      onChange={(value) => props.goto(value)}
      value={props.currentPath}
    >
      <Tab label="Counter" value="/counter" />
      <Tab label="Zen" value="/zen" />
    </Tabs>
    <Drawer
      docked={false}
      width={400}
      open={props.toggled}
      onRequestChange={props.toggleMenu}
    >
      <MenuItem onTouchTap={props.toggleMenu}>Close Menu</MenuItem>
      <MenuItem onTouchTap={props.startSaga}>Close in 1 second</MenuItem>
    </Drawer>
  </div>
);

Header.propTypes = {
  toggled: React.PropTypes.bool.isRequired,
  toggleMenu: React.PropTypes.func.isRequired,
  currentPath: React.PropTypes.string.isRequired,
  goto: React.PropTypes.func.isRequired,
  startSaga: React.PropTypes.func.isRequired,
};

export default Header;
