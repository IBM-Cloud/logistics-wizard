import { combineReducers } from 'redux';
import { routerReducer as router } from 'react-router-redux';
// import exampleReducer from 'modules/exampleModule';

export const makeRootReducer = (asyncReducers) =>
  combineReducers({
    // menu: exampleReducer,
    router,
    ...asyncReducers,
  });

export const injectReducer = (store, { key, reducer }) => {
  store.asyncReducers[key] = reducer; //eslint-disable-line
  store.replaceReducer(makeRootReducer(store.asyncReducers));
};

export default makeRootReducer;
