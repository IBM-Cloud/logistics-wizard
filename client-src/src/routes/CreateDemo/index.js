import { injectReducer } from 'store/reducers';
import { injectSagas } from 'store/sagas';

export default (store) => ({
  path: 'create-demo',
  getComponent(nextState, cb) {
    require.ensure([], (require) => {
      const CreateDemo = require('./containers/CreateDemoContainer').default;
      const reducer = require('./modules/CreateDemo').default;
      const sagas = require('./modules/CreateDemo').sagas;

      injectReducer(store, { key: 'createDemo', reducer });
      injectSagas(store, { key: 'createDemo', sagas });

      cb(null, CreateDemo);
    }, 'createDemo');
  },
});
