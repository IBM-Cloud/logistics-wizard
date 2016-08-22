import React from 'react';
import classNames from 'classnames';
import classes from './RoleItem.scss';

export class RoleItem extends React.Component {
  getItemType = () => {
    if (this.props.type === 'button') {
      return (
        <p
          className={classNames({
            [classes.label]: true,
            [classes.center]: true,
            [classes.button]: true,
          })}
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
          [classes.center]: true,
        })}
      >
        {this.props.label}
      </p>
    );
  }
  render() {
    return (
      <button
        className={classNames({
          [classes.item]: true,
          [classes.selected]: this.props.selected,
        })}
      >
        <div className={classes.iconContainer}>
          {this.props.type === 'button'
            ? <i
              className={classNames({
                [classes.icon]: true,
                [classes.small]: true,
                [this.props.icon]: true,
                fa: true,
              })}
            />
            : <i
              className={classNames({
                [classes.icon]: true,
                [this.props.icon]: true,
                fa: true,
              })}
            />
          }
        </div>

        <div className={classes.textContainer}>
          {this.getItemType()}
        </div>
      </button>
    );
  }
}

RoleItem.propTypes = {
  selected: React.PropTypes.bool,
  type: React.PropTypes.string,
  location: React.PropTypes.string,
  icon: React.PropTypes.string.isRequired,
  label: React.PropTypes.string.isRequired,
};

export default RoleItem;
