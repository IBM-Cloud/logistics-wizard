import React from 'react';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import classes from './CreateDemo.scss';

const styles = {
  container: {
    display: 'flex',
    alignItems: 'stretch',
  },
  button: {
    float: 'right',
    marginTop: '2rem',
  },
  fields: {
    width: '100%',
  },
};

export const CreateDemo = (props) => (
  <Paper style={styles.container} rounded>
    <div className={classes.leftBar} />
    <div className={classes.infoSection}>
      <h2>Create Demo Session</h2>
      <p>We promise to never bug you. While not necessary, providing us with your email address gives us an easy way to send you an email with your unique session ID.</p>
      <p className="thin">Already created a project? You can access a previous created session using the link sent to the email provided to us.</p>
    </div>
    <div className={classes.mainSection}>
      <p>Give your project a name</p>
      <TextField style={styles.fields} hintText="Supply Chain Logistics" />
      <p>Enter your email address (Optional)</p>
      <TextField style={styles.fields} hintText="UserName@business.com" />
      <br />
      <RaisedButton style={styles.button} label="LET'S GO" onClick={props.createDemo} />
    </div>
  </Paper>
);

CreateDemo.propTypes = {
  createDemo: React.PropTypes.func.isRequired,
};

export default CreateDemo;
