// We only need to import the modules necessary for initial render
import CoreLayout from '../layouts/CoreLayout/CoreLayout';
import Home from './Home';
import CounterRoute from './Counter';
import ZenRoute from './Zen';
import StylesRoute from './Styles';

/*  Note: Instead of using JSX, we recommend using react-router
    PlainRoute objects to build route definitions.   */

export const createRoutes = (store) => ({
  path: '/',
  component: CoreLayout,
  indexRoute: Home,
  childRoutes: [
    ZenRoute(store),
    CounterRoute(store),
    StylesRoute(),
  ],
});

export default createRoutes;
