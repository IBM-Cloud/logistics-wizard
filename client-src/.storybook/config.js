import { configure, addDecorator } from '@kadira/storybook';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import centered from '@kadira/react-storybook-decorator-centered';
import muiTheme from 'styles/muiTheme';
import '../src/styles/core.scss';

injectTapEventPlugin();
const rootStories = require.context('./stories/', true, /\.js$/);
const srcStories = require.context('../src/', true, /\.story\.js$/);
function loadStories() {
  rootStories.keys().forEach(rootStories);
  srcStories.keys().forEach(srcStories);
}

addDecorator(centered);
addDecorator((story) => (
  <MuiThemeProvider muiTheme={muiTheme}>
    {story()}
  </MuiThemeProvider>
));

configure(loadStories, module);
