// ------------------------------------
// Constants
// ------------------------------------
export const REQUEST_ZEN = 'REQUEST_ZEN';
export const RECEIVE_ZEN = 'RECEIVE_ZEN';
export const SAVE_CURRENT_ZEN = 'SAVE_CURRENT_ZEN';

// ------------------------------------
// Actions
// ------------------------------------
export const requestZen = () => ({
  type: REQUEST_ZEN,
});

let availableId = 0;
export const receiveZen = (value) => ({
  type: RECEIVE_ZEN,
  payload: {
    value,
    id: availableId++,
  },
});

export const saveCurrentZen = () => ({
  type: SAVE_CURRENT_ZEN,
});

export const fetchZen = () => (dispatch) => {
  dispatch(requestZen());

  return fetch('https://api.github.com/zen')
    .then(data => data.text())
    .then(text => dispatch(receiveZen(text)));
};

export const actions = {
  requestZen,
  receiveZen,
  fetchZen,
  saveCurrentZen,
};

// ------------------------------------
// Action Handlers
// ------------------------------------
const ZEN_ACTION_HANDLERS = {
  [REQUEST_ZEN]: (state) => ({ ...state, fetching: true }),
  [RECEIVE_ZEN]: (state, action) => ({
    ...state,
    zens: state.zens.concat(action.payload),
    current: action.payload.id,
    fetching: false,
  }),
  [SAVE_CURRENT_ZEN]: (state) => {
    return state.current != null
      ? ({ ...state, saved: state.saved.concat(state.current) })
      : state;
  },
};

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  fetching: false,
  current: null,
  zens: [],
  saved: [],
};

const zenReducer = (state = initialState, action) => {
  const handler = ZEN_ACTION_HANDLERS[action.type];

  return handler ? handler(state, action) : state;
};
export default zenReducer;
