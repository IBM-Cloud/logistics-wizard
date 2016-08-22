import { connect } from 'react-redux';
import { getQuote } from '../modules/Example';
import Example from '../components/Example';

const mapActionCreators = {
  actionAndSaga: () => getQuote(),
};

const mapStateToProps = (state) => ({
  title: state.example.title,
  quote: state.example.quote,
});

export default connect(mapStateToProps, mapActionCreators)(Example);
