// ---------------------------------------
// Test Environment Setup
// ---------------------------------------
const mockCssModules = require('mock-css-modules');
mockCssModules.register(['.sass', '.scss']);

// Ignore assets
require.extensions['.jpg'] = noop => noop;
require.extensions['.jpeg'] = noop => noop;
require.extensions['.png'] = noop => noop;
require.extensions['.gif'] = noop => noop;
require.extensions['.svg'] = noop => noop;

global.document = require('jsdom').jsdom('<body></body>');
global.window = document.defaultView;
global.navigator = window.navigator;
