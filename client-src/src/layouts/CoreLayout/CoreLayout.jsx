import React from 'react';
import 'styles/core.scss';
import classes from './CoreLayout.scss';

export const CoreLayout = ({ children }) => (
  <div className={classes.layoutContainer}>
    <div className={classes.mainContainer}>
      {children}
    </div>
  </div>
);

CoreLayout.propTypes = {
  children: React.PropTypes.element.isRequired,
};

export default CoreLayout;
