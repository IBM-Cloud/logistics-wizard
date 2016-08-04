import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import classes from './<%= pascalEntityName %>.scss';

export const <%= pascalEntityName %> = (props) => (
  <div>
    <h1><%= pascalEntityName %></h1>
    <h2 className={classes.<%= pascalEntityName %>Container}>
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

<%= pascalEntityName %>.propTypes = {
  counter: React.PropTypes.number.isRequired,
  doubleAsync: React.PropTypes.func.isRequired,
  increment: React.PropTypes.func.isRequired,
};

export default <%= pascalEntityName %>;
