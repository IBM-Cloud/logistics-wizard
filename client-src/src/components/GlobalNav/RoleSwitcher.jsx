import React from 'react';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
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
  left: {
    width: '32px',
    margin: 0,
    padding: 0,
    display: 'inline-block',
    float: 'left',
    marginRight: '20px',
  },
  menuCircle: {
    fontSize: 34,
    color: 'rgb(72, 85, 102)',
    lineHeight: '24px',
  },
  menuUser: {
    fontSize: 26,
    color: 'rgb(255, 255, 255)',
    lineHeight: '32px',
    marginLeft: '2px',
  },
  menuItem: {
    width: '300px',
  },
  listStyle: {
    marginTop: '0px',
  },
  menuPlus: {
    fontSize: 24,
  },
  innerListItem: {
    background: 'rgb(255, 255, 255)',
  },
};

// Try to figure out how to move the menus down. If you can't figure it out, skip for now. =)
export const RoleSwitcher = (props) => (
  <IconMenu
    menuStyle={styles.listStyle}
    open={props.open || null}
    anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
    iconButtonElement={
      <span className="fa-stack" style={styles.stack}>
        <i className="fa fa-circle fa-stack-2x" style={styles.circle} />
        <i className="fa fa-user fa-stack-1x" style={styles.user} />
      </span>
    }
  >
    <MenuItem
      innerDivStyle={styles.innerListItem}
      leftIcon={
        <span className="fa-stack">
          <i className="fa fa-circle fa-stack-2x" style={styles.menuCircle} />
          <i className="fa fa-user fa-stack-1x" style={styles.menuUser} />
        </span>
      }
    >
      <p className="roleSwitcherLabel"><strong>Supply Chain Manager</strong></p>
    </MenuItem>
    <MenuItem
      innerDivStyle={styles.innerListItem}
      leftIcon={
        <span className="fa-stack">
          <i className="fa fa-circle fa-stack-2x" style={styles.menuCircle} />
          <i className="fa fa-user fa-stack-1x" style={styles.menuUser} />
        </span>
      }
    >
      <p className="roleSwitcherLabel"><strong>Retail Manager</strong></p>
      <p className="roleSwitcherLabel"><em><small>Austin, Texas</small></em></p>
    </MenuItem>
    <MenuItem
      innerDivStyle={styles.innerListItem}
      leftIcon={
        <i className="fa fa-plus" style={styles.menuPlus} />
      }
    >
      <p>CREATE NEW RETAIL MANAGER</p>
    </MenuItem>
  </IconMenu>
);

RoleSwitcher.propTypes = {
  open: React.PropTypes.bool,
};

export default RoleSwitcher;
