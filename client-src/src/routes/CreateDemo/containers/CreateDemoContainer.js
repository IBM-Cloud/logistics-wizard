import { connect } from 'react-redux';
import { getQuote } from '../modules/CreateDemo';
import CreateDemo from '../components/CreateDemo';

const mapActionCreators = {
  actionAndSaga: () => getQuote(),
};

const mapStateToProps = (state) => ({
  title: state.createDemo.title,
  quote: state.createDemo.quote,
});

export default connect(mapStateToProps, mapActionCreators)(CreateDemo);
