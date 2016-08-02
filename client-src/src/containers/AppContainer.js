import React, { PropTypes } from 'react';
import { Router } from 'react-router';
import { Provider } from 'react-redux';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

const AppContainer = (props) => {
  const { history, routes, store } = props;

  return (
    <Provider store={store}>
      <MuiThemeProvider>
        <div style={{ height: '100%' }}>
          <Router history={history} children={routes} />
        </div>
      </MuiThemeProvider>
    </Provider>
  );
};

AppContainer.propTypes = {
  history: PropTypes.object.isRequired,
  routes: PropTypes.object.isRequired,
  store: PropTypes.object.isRequired,
};

export default AppContainer;
