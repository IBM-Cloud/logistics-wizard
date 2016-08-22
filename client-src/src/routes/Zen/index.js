import { injectReducer } from 'store/reducers';
import { injectSagas } from 'store/sagas';

export default (store) => ({
  path: 'zen',
  getComponent(nextState, cb) {
    require.ensure([
      './containers/ZenContainer',
      './modules/zen',
    ], (require) => {
      const Zen = require('./containers/ZenContainer').default;
      const reducer = require('./modules/zen').default;
      const sagas = require('./modules/zen').sagas;

      injectReducer(store, { key: 'zen', reducer });
      injectSagas(store, { key: 'zen', sagas });
      cb(null, Zen);
    }, 'zen');
  },
});
