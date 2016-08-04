import { connect } from 'react-redux';
import { getQuote } from '../modules/<%= pascalEntityName %>';
import <%= pascalEntityName %> from '../components/<%= pascalEntityName %>';

const mapActionCreators = {
  actionAndSaga: () => getQuote(),
};

const mapStateToProps = (state) => ({
  title: state.<%= camelEntityName %>.title,
  quote: state.<%= camelEntityName %>.quote,
});

export default connect(mapStateToProps, mapActionCreators)(<%= pascalEntityName %>);
