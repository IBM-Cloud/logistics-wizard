import React from 'react';
import classNames from 'classnames';
import classes from './RoleItem.scss';

export class RoleItem extends React.Component {
  getItemType = () => {
    if (this.props.type === 'button') {
      return (
        <p
          className={classes.label}
          style={{ paddingTop: '10px', fontWeight: '500', paddingBottom: '12px', cursor: 'pointer' }}
        >
            {this.props.label}
        </p>
      );
    }
    else if (this.props.location) {
      return (
        <div>
          <p className={classes.label}>{this.props.label}</p>
          <p className={classes.sublabel}>{this.props.location}</p>
        </div>
      );
    }

    return (
      <p
        className={classNames({
          [classes.label]: true,
          [classes.padTop]: true,
        })}
      >
        {this.props.label}
      </p>
    );
  }
  render() {
    return (
      <div className={classes.roleItem}>
        <div className={classes.roleIcon}>
          {this.props.type === 'button'
            ? <i
              className={classNames({
                [classes.plus]: true,
                fa: true,
                'fa-plus': true,
              })}
            />
            : <span className="fa-stack">
              <i
                className={classNames({
                  [classes.circle]: true,
                  fa: true,
                  'fa-circle': true,
                  'fa-stack-2x': true,
                })}
              />
              <i
                className={classNames({
                  [classes.user]: true,
                  fa: true,
                  'fa-user': true,
                  'fa-stack-1x': true,
                })}
              />
            </span>
          }
        </div>

        <div className="roleText">
          {this.getItemType()}
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
  label: React.PropTypes.string.isRequired,
  location: React.PropTypes.string,
};

export default RoleItem;
