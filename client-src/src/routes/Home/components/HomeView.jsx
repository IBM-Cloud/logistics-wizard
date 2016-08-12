import React from 'react';
import classes from './HomeView.scss';
import CreateDemo from 'routes/CreateDemo/components/CreateDemo';

export const HomeView = () => (
  <div className={classes.homeView}>
    <h1>Logistics Wizard</h1>
    <h4>TODO: Build "landing page" here</h4>
    <CreateDemo />
  </div>
);

export default HomeView;
