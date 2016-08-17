import React from 'react';
import RoleItem from './RoleItem';
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
  menuPlus: {
    fontSize: 24,
    marginLeft: '2px',
  },
  menuLabel: {
    margin: 0,
    padding: 0,
    textTransform: 'uppercase',
    fontSize: 14,
  },
  menuSublabel: {
    margin: 0,
    padding: 0,
    lineHeight: '10px',
    marginTop: '-5px',
  },
  listStyle: {
    marginTop: '0px',
    padding: '0px',
  },
  innerListItem: {
    background: 'rgb(255, 255, 255)',
    margin: '10px 0px',
    verticalAlign: 'center',
    height: '60px',
    lineHeight: '50px',
  },
};

// Try to figure out how to move the menus down. If you can't figure it out, skip for now. =)
export const RoleSwitcher = (props) => (
  <IconMenu
    style={{ padding: '0px' }}
    innerDivStyle={{ padding: '0px' }}
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
    <RoleItem label="Supply Chain Manager" />
    <RoleItem label="Retail Manager" location="Austin, Texas" />
    <RoleItem label="Retail Manager" location="Chino, California" />
    <RoleItem label="Create New Retail Manager" type="button" />
  </IconMenu>
);

RoleSwitcher.propTypes = {
  open: React.PropTypes.bool,
};

export default RoleSwitcher;
