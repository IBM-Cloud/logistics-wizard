import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import classes from './Counter.scss';

const Counter = (props) => (
  <div>
    <h2 className={classes.counterContainer}>
      Counter:
      {' '}
      <span className={classes['counter--green']}>
        {props.counter}
      </span>
    </h2>
    <RaisedButton label="Increment" onClick={props.increment} />
    {' '}
    <RaisedButton label="Double (Async)" onClick={props.doubleAsync} />
  </div>
);

Counter.propTypes = {
  counter: React.PropTypes.number.isRequired,
  doubleAsync: React.PropTypes.func.isRequired,
  increment: React.PropTypes.func.isRequired,
};

export default Counter;
