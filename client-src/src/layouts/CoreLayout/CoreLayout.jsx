import React from 'react';
import GlobalNav from 'components/GlobalNav';
import 'styles/core.scss';
import classes from './CoreLayout.scss';

export const CoreLayout = ({ children }) => (
  <div className={classes.layoutContainer}>
    <GlobalNav />
    <div className={classes.mainContainer}>
      {children}
    </div>
  </div>
);

CoreLayout.propTypes = {
  children: React.PropTypes.element.isRequired,
};

export default CoreLayout;
