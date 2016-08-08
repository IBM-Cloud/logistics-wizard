/* eslint-disable */

import { argv } from 'yargs';
import fs from 'fs';

// Needed to avoid errors with requiring css modules from js
const mockCssModules = require('mock-css-modules');
mockCssModules.register(['.sass', '.scss']);

// Since fetch doesn't work in node, this is needed for testing api calls
require('isomorphic-fetch');

// Ignore assets
require.extensions['.jpg'] = noop => noop;
require.extensions['.jpeg'] = noop => noop;
require.extensions['.png'] = noop => noop;
require.extensions['.gif'] = noop => noop;
require.extensions['.svg'] = noop => noop;

// Set up dom
require.extensions['.html'] = (module, filename) => {
  module.exports = fs.readFileSync(filename, 'utf8');
}

global.document = require('jsdom').jsdom(require('../src/index.html'));
global.window = document.defaultView;
global.navigator = window.navigator;

// Set up project globals
const env = process.env.NODE_ENV || 'development';
global.process.env = {
  'NODE_ENV' : JSON.stringify(env),
};
global['NODE_ENV'] = env;
global['__DEV__'] = env === 'development';
global['__PROD__'] = env === 'production';
global['__TEST__'] = env === 'test';
global['__DEBUG__'] = env === 'development' && !argv.no_debug;
global['__COVERAGE__'] = !argv.watch && env === 'test';
global['__BASENAME__'] = JSON.stringify(process.env.BASENAME || '');
