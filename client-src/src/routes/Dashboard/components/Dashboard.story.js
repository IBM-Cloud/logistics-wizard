import React from 'react';
import { storiesOf, action, linkTo } from '@kadira/storybook';
import Dashboard from './Dashboard';

storiesOf('Dashboard', module)
  .add('default state', () => (
    <Dashboard
      title="Hi I am the title prop!"
      quote="Click the button to receive a quote."
      actionAndSaga={linkTo('Dashboard', 'fetching quote')}
    />
  ))
  .add('fetching quote', () => (
    <Dashboard
      title="You dispatched an action!"
      quote="Fetching quote..."
      actionAndSaga={linkTo('Dashboard', 'quote fetched')}
    />
  ))
  .add('quote fetched', () => (
    <Dashboard
      title="You dispatched an action!"
      quote="If you aren't living, then you are dying."
      actionAndSaga={linkTo('Dashboard', 'additional clicks')}
    />
  ))
  .add('additional clicks', () => (
    <Dashboard
      title="You already received a quote."
      quote="If you aren't living, then you are dying."
      actionAndSaga={action('No additional actions')}
    />
  ));
