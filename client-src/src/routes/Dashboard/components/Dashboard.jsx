import React from 'react';
import classes from './Dashboard.scss';

export const Dashboard = (props) => (
  <div className={classes.dashboard}>
    <h4>Dashboard - {props.title}</h4>
    <button onClick={props.actionAndSaga}>Click Me!</button>
    <h4>{props.quote || 'Click button to receive a quote.'}</h4>
  </div>
);

Dashboard.propTypes = {
  title: React.PropTypes.string.isRequired,
  quote: React.PropTypes.string,
  actionAndSaga: React.PropTypes.func.isRequired,
};

export default Dashboard;
