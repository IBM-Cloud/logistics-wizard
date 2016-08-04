import React from 'react';
import { push } from 'react-router-redux';
import AppBar from 'material-ui/AppBar';
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
      showMenuIconButton={false}
      onTitleTouchTap={() => props.dispatch(push('/'))}
    />
    <Tabs
      onChange={(value) => props.dispatch(push(value))}
      value={props.currentPath}
    >
      <Tab label="Styles" value="/styles" />
      <Tab label="Counter" value="/counter" />
      <Tab label="Zen" value="/zen" />
    </Tabs>
  </div>
);

Header.propTypes = {
  dispatch: React.PropTypes.func.isRequired,
  currentPath: React.PropTypes.string.isRequired,
};

export default Header;
