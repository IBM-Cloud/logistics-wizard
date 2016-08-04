/* eslint-disable no-unused-expressions */

import <%= pascalEntityName %>Route from './';

describe('(Route) <%= pascalEntityName %>', () => {
  let route;

  beforeEach(() => {
    route = <%= pascalEntityName %>Route({});
  });

  it('Should return a route configuration object', () => {
    expect(typeof (route)).to.equal('object');
  });

  it('Configuration should contain path `<%= dashesEntityName %>`', () => {
    expect(route.path).to.equal('<%= dashesEntityName %>');
  });
});
