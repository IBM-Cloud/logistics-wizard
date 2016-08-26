import React from 'react';
import IconMenu from 'material-ui/IconMenu';
import { Icon } from 'react-fa';
import RoleItem from './RoleItem';
import classNames from 'classnames';
import classes from './GlobalNav.scss';

const styles = {
  stack: {
    position: 'relative',
    cursor: 'pointer',
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

// Props have been removed since they are not currently needed.
// To add props back in, simply change the line below to: ...RoleSwitcher = (props) => (...
export const RoleSwitcher = () => (
  <IconMenu
    // anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
    iconButtonElement={
      <span className={classes.stack}>
        <Icon
          stack="2x"
          name="circle"
          className={classes.circle}
        />
        <Icon
          stack="1x"
          name="user"
          className={classes.user}
        />
      </span>
      // <span
      //   className={classNames({
      //     'fa-stack': true,
      //     [classes.stack]: true,
      //   })}
      // >
      //   <i
      //     className={classNames({
      //       fa: true,
      //       'fa-circle': true,
      //       'fa-stack-2x': true,
      //       [classes.circle]: true,
      //     })}
      //   />
      //   <i
      //     className={classNames({
      //       fa: true,
      //       'fa-user': true,
      //       'fa-stack-1x': true,
      //       [classes.user]: true,
      //     })}
      //   />
      // </span>
    }
  >
    <RoleItem label="Supply Chain Manager" icon="fa-user" />
    <RoleItem label="Retail Manager" location="Austin, Texas" icon="fa-user" selected="true" />
    <RoleItem label="Retail Manager" location="Chino, California" icon="fa-user" />
    <RoleItem label="Create New Retail Manager" type="button" icon="fa-plus" />
  </IconMenu>
);

RoleSwitcher.propTypes = {};

export default RoleSwitcher;
