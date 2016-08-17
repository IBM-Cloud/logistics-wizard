import React from 'react';
import FontIcon from 'material-ui/FontIcon';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import IconButton from 'material-ui/IconButton';
import RoleSwitcher from './RoleSwitcher';
import { Toolbar, ToolbarGroup, ToolbarTitle, ToolbarSeparator } from 'material-ui/Toolbar';
import classes from './GlobalNav.scss';

const styles = {
  toolbar: {
    backgroundColor: 'rgb(15, 147, 166)',
  },
  title: {
    paddingLeft: '2rem',
    color: 'rgb(255, 255, 255)',
    fontSize: '1rem',
  },
  separator: {
    backgroundColor: 'rgb(255, 255, 255)',
  },
  paragraph: {
    paddingLeft: '2rem',
    fontSize: '0.9rem',
  },
  stack: {
    position: 'relative',
    cursor: 'pointer',
  },
  github: {
    color: 'rgb(255, 255, 255)',
    fontSize: 34,
  },
  user: {
    fontSize: 30,
    color: 'rgb(15, 147, 166)',
    lineHeight: '62px',
  },
  circle: {
    fontSize: 34,
    color: 'rgb(255, 255, 255)',
    lineHeight: '56px',
  },
};

export const GlobalNav = (props) => (
  <div className={classes.globalNav}>
    <Toolbar style={styles.toolbar}>
      <ToolbarGroup firstChild>
        <ToolbarTitle text="Logistics Wizard" className="" style={styles.title} />
      </ToolbarGroup>

      <ToolbarGroup>
        <RoleSwitcher />
        <ToolbarSeparator style={styles.separator} />
        <FontIcon className="fa fa-github" style={styles.github} />
        <p className="flow-text" style={styles.paragraph}>Demo Settings</p>
      </ToolbarGroup>
    </Toolbar>
  </div>
);

GlobalNav.propTypes = {
  customProp: React.PropTypes.string,
  open: React.PropTypes.bool,
};

export default GlobalNav;
