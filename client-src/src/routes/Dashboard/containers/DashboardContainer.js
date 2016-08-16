import { connect } from 'react-redux';
import { getQuote } from '../modules/Dashboard';
import Dashboard from '../components/Dashboard';

const mapActionCreators = {
  actionAndSaga: () => getQuote(),
};

const mapStateToProps = (state) => ({
  title: state.dashboard.title,
  quote: state.dashboard.quote,
});

export default connect(mapStateToProps, mapActionCreators)(Dashboard);
