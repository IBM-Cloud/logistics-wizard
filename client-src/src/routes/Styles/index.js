export default () => ({
  path: 'styles',
  getComponent(nextState, cb) {
    require.ensure([
      './components/Styles',
    ], (require) => {
      const Styles = require('./components/Styles').default;

      cb(null, Styles);
    }, 'styles');
  },
});
