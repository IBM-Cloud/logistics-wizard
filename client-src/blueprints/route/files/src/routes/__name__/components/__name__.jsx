import React from 'react';
import classes from './<%= pascalEntityName %>.scss';

export const <%= pascalEntityName %> = (props) => (
  <div className={classes.<%= camelEntityName %>}>
    <h4><%= pascalEntityName %> - {props.title}</h4>
    <button onClick={props.actionAndSaga}>Click Me!</button>
    <h4>{props.quote || 'Click button to receive a quote.'}</h4>
  </div>
);

<%= pascalEntityName %>.propTypes = {
  title: React.PropTypes.string.isRequired,
  quote: React.PropTypes.string,
  actionAndSaga: React.PropTypes.func.isRequired,
};

export default <%= pascalEntityName %>;
