import { configure, addDecorator } from '@kadira/storybook';
import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import centered from '@kadira/react-storybook-decorator-centered';
import '../src/styles/core.scss';

function loadStories() {
  require('./stories/Zen');
}

addDecorator(centered);
addDecorator((story) => (
  <MuiThemeProvider muiTheme={getMuiTheme()}> 
    {story()}
  </MuiThemeProvider>
));

configure(loadStories, module);
