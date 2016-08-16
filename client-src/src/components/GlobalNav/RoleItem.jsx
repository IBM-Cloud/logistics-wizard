import React from 'react';
import classes from './RoleItem.scss';

const styles = {
  circle: {
    fontSize: 36,
    color: 'rgb(72, 85, 102)',
    lineHeight: '26px',
  },
  user: {
    fontSize: 28,
    color: 'rgb(255, 255, 255)',
    lineHeight: '34px',
  },
};

export class RoleItem extends React.Component {
  render() {
    return (
      <div className={classes.roleItem}>
        <div className={classes.roleIcon}>
          <span className="fa-stack">
            <i className="fa fa-circle fa-stack-2x" style={styles.circle} />
            <i className="fa fa-user fa-stack-1x" style={styles.user} />
          </span>
        </div>

        <div className="roleText">
          {/* How can we pass this data through propTypes? */}

          {this.props.location
            ? <p className={classes.label}>{this.props.roleLabel}</p>
            : <p className={classes.label} style={{ paddingTop: '10px' }}>{this.props.roleLabel}</p>
          }

          {this.props.location
            ?
            <p className={classes.sublabel}>{this.props.location}</p>
            : ''
          }
        </div>
      </div>
    );
  }
}

RoleItem.propTypes = {
  // open: React.PropTypes.bool,
  roleLabel: React.PropTypes.string.isRequired,
  location: React.PropTypes.string,
};

export default RoleItem;
