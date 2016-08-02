import { connect } from 'react-redux';
import Header from './Header';

const mapStateToProps = (state) => ({
  currentPath: state.router.locationBeforeTransitions.pathname,
});

export default connect(mapStateToProps)(Header);
