import React from 'react';
import classes from './Example.scss';

export const Example = (props) => (
  <div className={classes.example}>
    <h4>Example - {props.title}</h4>
    <button onClick={props.actionAndSaga}>Click Me!</button>
    <h4>{props.quote || 'Click button to receive a quote.'}</h4>
  </div>
);

Example.propTypes = {
  title: React.PropTypes.string.isRequired,
  quote: React.PropTypes.string,
  actionAndSaga: React.PropTypes.func.isRequired,
};

export default Example;
