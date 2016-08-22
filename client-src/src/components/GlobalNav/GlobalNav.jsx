import React from 'react';
import IconButton from 'material-ui/IconButton';
import { Toolbar, ToolbarGroup, ToolbarTitle, ToolbarSeparator } from 'material-ui/Toolbar';
import { Icon } from 'react-fa';
import RoleSwitcher from './RoleSwitcher';
import classes from './GlobalNav.scss';

const styles = {
  toolbar: {
    backgroundColor: 'rgb(15, 147, 166)',
  },
  separator: {
    backgroundColor: 'rgb(184, 222, 228)',
    margin: '0px 12px 0px 24px',
  },
  paragraph: {
    paddingLeft: '2rem',
    fontSize: '0.9rem',
  },
  title: {
    color: 'rgb(255, 255, 255)',
    fontSize: '1rem',
  },
};

export const GlobalNav = () => (
  <div className={classes.globalNav}>
    <Toolbar style={styles.toolbar}>
      <ToolbarGroup firstChild>
        <ToolbarTitle text="Logistics Wizard" className={classes.title} style={styles.title} />
      </ToolbarGroup>

      <ToolbarGroup>
        <RoleSwitcher />
        <ToolbarSeparator style={styles.separator} />
        <IconButton>
          <Icon
            name="github"
            className={classes.github}
          />
        </IconButton>
        <p className="flow-text" style={styles.paragraph}>Demo Settings</p>
      </ToolbarGroup>
    </Toolbar>
  </div>
);

GlobalNav.propTypes = {};

export default GlobalNav;
