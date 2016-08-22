import React from 'react';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import classNames from 'classnames';
import { applyContainerQuery } from 'react-container-query';
import classes from './CreateDemo.scss';

export class CreateDemo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      demoName: '',
      email: '',
    };
  }

  handleInput = (event) => {
    this.setState({
      [event.target.id]: event.target.value,
    });
  }

  handleClick = () => {
    const body = { name: this.state.demoName };
    if (this.state.email !== '') body.email = this.state.email;
    this.props.createDemo(body);
  }

  render() {
    const { full } = this.props.containerQuery;

    return (
      <Paper className={classes.container}>
        <div
          className={classNames({
            [classes.infoSection]: true,
            [classes.full]: full,
          })}
        >
          <h4 className={classes.title}>Create Demo Session</h4>
          <p>We promise to never bug you. While not necessary, providing us with your email address gives us an easy way to send you an email with your unique session ID.</p>
          <p className="thin">Already created a project? You can access a previous created session using the link sent to the email provided to us.</p>
        </div>
        <div className={classes.mainSection}>
          <div className={classes.inputs}>
            <TextField
              id="demoName"
              fullWidth
              value={this.state.demoName}
              floatingLabelText="Give your project a name"
              floatingLabelFixed
              hintText="Supply Chain Logistics"
              onChange={this.handleInput}
            />
            <TextField
              id="email"
              fullWidth
              value={this.state.email}
              floatingLabelText="Enter your email address (optional)"
              floatingLabelFixed
              hintText="UserName@business.com"
              onChange={this.handleInput}
            />
          </div>
          <div className={classes.buttonWrapper}>
            <RaisedButton
              primary
              className={classes.button}
              label="CREATE DEMO"
              onClick={this.handleClick}
            />
          </div>
        </div>
      </Paper>
    );
  }
}

CreateDemo.propTypes = {
  createDemo: React.PropTypes.func.isRequired,
  containerQuery: React.PropTypes.object,
};

const query = {
  full: {
    minWidth: 773,
  },
};

export default applyContainerQuery(CreateDemo, query);
