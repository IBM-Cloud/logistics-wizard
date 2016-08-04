import { configure, addDecorator } from '@kadira/storybook';
import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import centered from '@kadira/react-storybook-decorator-centered';
import '../src/styles/core.scss';

const rootStories = require.context('./stories/', true, /\.js$/);
const srcStories = require.context('../src/', true, /\.story\.js$/);
function loadStories() {
  rootStories.keys().forEach(rootStories);
  srcStories.keys().forEach(srcStories);
}

addDecorator(centered);
addDecorator((story) => (
  <MuiThemeProvider muiTheme={getMuiTheme()}>
    {story()}
  </MuiThemeProvider>
));

configure(loadStories, module);
