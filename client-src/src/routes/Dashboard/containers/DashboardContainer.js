import { connect } from 'react-redux';
// import { getQuote } from '../modules/Dashboard';
import Dashboard from '../components/Dashboard';

const mapActionCreators = {
};

const mapStateToProps = (state) => ({
  demoName: state.demoSession.name,
});

export default connect(mapStateToProps, mapActionCreators)(Dashboard);
