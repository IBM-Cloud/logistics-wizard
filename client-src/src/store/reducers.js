import { combineReducers } from 'redux';
import { routerReducer as router } from 'react-router-redux';
import demos from 'modules/demos';

export const makeRootReducer = (asyncReducers) =>
  combineReducers({
    demoSession: demos,
    router,
    ...asyncReducers,
  });

export const injectReducer = (store, { key, reducer }) => {
  store.asyncReducers[key] = reducer; //eslint-disable-line
  store.replaceReducer(makeRootReducer(store.asyncReducers));
};

export default makeRootReducer;
