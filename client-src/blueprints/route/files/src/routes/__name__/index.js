import { injectReducer } from 'store/reducers';
import { injectSagas } from 'store/sagas';

export default (store) => ({
  path: '<%= dashesEntityName %>',
  getComponent(nextState, cb) {
    require.ensure([], (require) => {
      const <%= pascalEntityName %> = require('./containers/<%= pascalEntityName %>Container').default;
      const reducer = require('./modules/<%= pascalEntityName %>').default;
      const sagas = require('./modules/<%= pascalEntityName %>').sagas;

      injectReducer(store, { key: '<%= camelEntityName %>', reducer });
      injectSagas(store, { key: '<%= camelEntityName %>', sagas });

      cb(null, <%= pascalEntityName %>);
    }, '<%= camelEntityName %>');
  },
});
