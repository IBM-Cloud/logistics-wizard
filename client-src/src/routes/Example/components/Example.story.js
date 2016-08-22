import React from 'react';
import { storiesOf, action, linkTo } from '@kadira/storybook';
import Example from './Example';

storiesOf('Example', module)
  .add('default state', () => (
    <Example
      title="Hi I am the title prop!"
      quote="Click the button to receive a quote."
      actionAndSaga={linkTo('Example', 'fetching quote')}
    />
  ))
  .add('fetching quote', () => (
    <Example
      title="You dispatched an action!"
      quote="Fetching quote..."
      actionAndSaga={linkTo('Example', 'quote fetched')}
    />
  ))
  .add('quote fetched', () => (
    <Example
      title="You dispatched an action!"
      quote="If you aren't living, then you are dying."
      actionAndSaga={linkTo('Example', 'additional clicks')}
    />
  ))
  .add('additional clicks', () => (
    <Example
      title="You already received a quote."
      quote="If you aren't living, then you are dying."
      actionAndSaga={action('No additional actions')}
    />
  ));
