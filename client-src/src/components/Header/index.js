import { connect } from 'react-redux';
// import { toggle, startSaga } from 'modules/exampleModule';
import { push } from 'react-router-redux';
import Header from './Header';

const mapStateToProps = (state) => ({
  currentPath: state.router.locationBeforeTransitions.pathname,
  // toggled: state.menu.toggled,
  toggled: false,
});

const mapActionCreators = {
  toggleMenu: () => () => {},
  goto: (route) => push(route),
  startSaga: () => () => {},
};

export default connect(mapStateToProps, mapActionCreators)(Header);
