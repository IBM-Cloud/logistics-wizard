export default () => ({
  path: 'styles',
  getComponent(nextState, cb) {
    require.ensure([
      './components/StylesView',
    ], (require) => {
      const StylesView = require('./components/StylesView').default;

      cb(null, StylesView);
    }, 'styles');
  },
});
