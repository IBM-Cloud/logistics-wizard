import React from 'react';
import classes from './HomeView.scss';
import RaisedButton from 'material-ui/RaisedButton';
import { Link } from 'react-router';

export const HomeView = () => (
  <div className={classes.homeView}>
    <h1>Logistics Wizard</h1>
    <h4>TODO: Build "landing page" here</h4>
    <Link to="/create-demo">Create new demo</Link>
  </div>
);

export default HomeView;
