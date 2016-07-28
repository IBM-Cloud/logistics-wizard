import { connect } from 'react-redux';
import { fetchZen, saveCurrentZen } from '../modules/zen';

import Zen from '../components/Zen';

/*  Object of action creators (can also be function that returns object).
    Keys will be passed as props to presentational components. Here we are
    implementing our wrapper around increment; the component doesn't care   */

const mapActionCreators = {
  fetchZen,
  saveCurrentZen,
};

const mapStateToProps = (state) => ({
  zen: state.zen.zens.find(zen => zen.id === state.zen.current),
  saved: state.zen.zens.filter(zen => state.zen.saved.indexOf(zen.id) !== -1),
});

export default connect(mapStateToProps, mapActionCreators)(Zen);
