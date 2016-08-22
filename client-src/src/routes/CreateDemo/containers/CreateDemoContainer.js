import { connect } from 'react-redux';
import { createDemo } from '../modules/CreateDemo';
import CreateDemo from '../components/CreateDemo';

const mapActionCreators = {
  createDemo,
};

const mapStateToProps = (state) => ({
});

export default connect(mapStateToProps, mapActionCreators)(CreateDemo);
