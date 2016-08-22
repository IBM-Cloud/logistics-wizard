import { injectReducer } from 'store/reducers';
import { injectSagas } from 'store/sagas';

export default (store) => ({
  path: 'example',
  getComponent(nextState, cb) {
    require.ensure([], (require) => {
      const Example = require('./containers/ExampleContainer').default;
      const reducer = require('./modules/Example').default;
      const sagas = require('./modules/Example').sagas;

      injectReducer(store, { key: 'example', reducer });
      injectSagas(store, { key: 'example', sagas });

      cb(null, Example);
    }, 'example');
  },
});
