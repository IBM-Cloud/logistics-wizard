import React from 'react';
import classes from './<%= pascalEntityName %>.scss';

export const <%= pascalEntityName %> = (props) => (
  <div className={classes.<%= camelEntityName %>}>
    <h1><%= pascalEntityName %></h1>
    <h2>Prop: {props.customProp || 'no prop given.'}</h2>
    <button onClick={props.clicky}>Clicky</button>
  </div>
);

<%= pascalEntityName %>.propTypes = {
  customProp: React.PropTypes.string,
  clicky: React.PropTypes.func.isRequired,
};

export default <%= pascalEntityName %>;
