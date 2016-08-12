import React from 'react';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import classes from './CreateDemo.scss';

const styles = {
  padding: '1rem',
};

export const CreateDemo = (props) => (
  <Paper style={styles} rounded>
    <p>Give your project a name (Optional)</p>
    <TextField hintText="Supply Chain Logistics" />
    <p>Enter your email address (Optional)</p>
    <TextField hintText="UserName@business.com" />
    <br />
    <RaisedButton label="LET'S GO" />
  </Paper>
);

CreateDemo.propTypes = {
};

export default CreateDemo;
