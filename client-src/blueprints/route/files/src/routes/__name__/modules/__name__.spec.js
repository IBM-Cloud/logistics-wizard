/* eslint-disable no-unused-expressions */

import { take, select } from 'redux-saga/effects';
import {
  COOL_ACTION,
  coolAction,
  default as <%= camelEntityName %>Reducer,
} from './<%= camelEntityName %>';

describe('(Redux Module) <%= pascalEntityName %>', () => {
  it('Should export a constant COUNTER_INCREMENT.', () => {
    expect(COUNTER_INCREMENT).to.equal('COUNTER_INCREMENT');
  });

  describe('(Reducer)', () => {
    it('Should be a function.', () => {
      expect(<%= camelEntityName %>Reducer).to.be.a('function');
    });

    it('Should initialize with a state of 0 (Number).', () => {
      expect(<%= camelEntityName %>Reducer(undefined, {})).to.equal('A Title Stored in global state.');
    });

    // it('Should return the previous state if an action was not matched.', () => {
    //   let state = counterReducer(undefined, {});
    //   expect(state).to.equal(0);
    //   state = counterReducer(state, { type: '@@@@@@@' });
    //   expect(state).to.equal(0);
    //   state = counterReducer(state, increment(5));
    //   expect(state).to.equal(5);
    //   state = counterReducer(state, { type: '@@@@@@@' });
    //   expect(state).to.equal(5);
    // });
  });

  // describe('(Action Creator) coolAction', () => {
  //   it('Should be exported as a function.', () => {
  //     expect(increment).to.be.a('function');
  //   });
  //
  //   it('Should return an action with type "COUNTER_INCREMENT".', () => {
  //     expect(increment()).to.have.property('type', COUNTER_INCREMENT);
  //   });
  //
  //   it('Should assign the first argument to the "payload" property.', () => {
  //     expect(increment(5)).to.have.property('payload', 5);
  //   });
  //
  //   it('Should default the "payload" property to 1 if not provided.', () => {
  //     expect(increment()).to.have.property('payload', 1);
  //   });
  // });

  // NOTE: if you have a more complex state, you will probably want to verify
  // that you did not mutate the state.
  // describe('(Action Handler) COOL_ACTION', () => {
  //   it('Should increment the state by the action payload\'s "value" property.', () => {
  //     let state = counterReducer(undefined, {});
  //     expect(state).to.equal(0);
  //     state = counterReducer(state, increment(1));
  //     expect(state).to.equal(1);
  //     state = counterReducer(state, increment(2));
  //     expect(state).to.equal(3);
  //     state = counterReducer(state, increment(-3));
  //     expect(state).to.equal(0);
  //   });
  // });

  // describe('(Saga) doubleAsync', () => {
  //   it('Should double the value', () => {
  //     const generator = doubleAsync();
  //     expect(generator.next().value).to.deep.equal(take(COUNTER_DOUBLE));
  //     expect(generator.next().value).to.deep.equal(select());
  //   });
  // });
});
