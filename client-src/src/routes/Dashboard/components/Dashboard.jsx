import React from 'react';
import classes from './Dashboard.scss';

export const Dashboard = (props) => (
  <div className={classes.dashboard}>
    <h4>Dashboard - Yay, you created a demo!</h4>
    <p>Demo Name: {props.demoName}</p>
  </div>
);

Dashboard.propTypes = {
  demoName: React.PropTypes.string.isRequired,
};

export default Dashboard;
