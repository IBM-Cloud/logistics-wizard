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
  plus: {
    fontSize: 24,
    color: 'rgb(72, 85, 102)',
    lineHeight: '24px',
    paddingLeft: '10px',
  },
};

export class RoleItem extends React.Component {
  render() {
    let roleText;

    if (this.props.type && this.props.type === 'button') {
      roleText = (
        <p
          className={classes.label}
          style={{ paddingTop: '10px', fontWeight: '500', paddingBottom: '12px', cursor: 'pointer' }}
        >
            {this.props.roleLabel}
        </p>
      );
    }
    else if (this.props.location) {
      roleText = (
        <div>
          <p className={classes.label}>{this.props.roleLabel}</p>
          <p className={classes.sublabel}>{this.props.location}</p>
        </div>
      );
    }
    else {
      roleText = (
        <p className={classes.label} style={{ paddingTop: '10px' }}>
          {this.props.roleLabel}
        </p>
      );
    }

    return (
      <div className={classes.roleItem}>
        <div className={classes.roleIcon}>
          {this.props.type === 'button'
            ? <i className="fa fa-plus" style={styles.plus} />
            : <span className="fa-stack">
              <i className="fa fa-circle fa-stack-2x" style={styles.circle} />
              <i className="fa fa-user fa-stack-1x" style={styles.user} />
            </span>
          }
        </div>

        <div className="roleText">
          {roleText}
        </div>
      </div>
    );
  }

  // someMethod(type, label, location) {
  //   let jsx;
  //   if (type && type === 'button') {
  //     jsx = (
  //       <p className={classes.label} style={{ paddingTop: '10px', fontWeight: '500' }}>{label}</p>
  //     );
  //   } else if (location) {
  //     jsx = (
  //       <div className="roleText">
  //         <p className={classes.label}>{label}</p>
  //         <p className={classes.sublabel}>{location}</p>
  //       </div>
  //     );
  //   } else {
  //     jsx = (
  //       <p className={classes.label} style={{ paddingTop: '10px' }}>{label}</p>
  //     );
  //   }
  //
  //   return jsx;
  // }
}

RoleItem.propTypes = {
  // open: React.PropTypes.bool,
  type: React.PropTypes.string,
  roleLabel: React.PropTypes.string.isRequired,
  location: React.PropTypes.string,
};

export default RoleItem;
