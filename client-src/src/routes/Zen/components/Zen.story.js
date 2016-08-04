import React from 'react';
import { storiesOf, action } from '@kadira/storybook';
import Zen from './Zen';

storiesOf('Zen', module)
  .add('No Zens', () => (
    <Zen
      zen={{}}
      saved={[]}
      requestZen={action('request zen')}
      saveCurrentZen={action('save current zen')}
    />
  ))
  .add('Fetched Zen - none saved', () => (
    <Zen
      zen={{ value: 'Speak like a human.', id: 0 }}
      saved={[]}
      requestZen={action('request zen')}
      saveCurrentZen={action('save current zen')}
    />
  ))
  .add('Fetched Zen - saved wisdoms', () => (
    <Zen
      zen={{ value: 'Speak like a human.', id: 3 }}
      saved={[
        {
          value: 'Some insightful quote',
          id: 0,
        },
        {
          value: 'Really funny quote',
          id: 1,
        },
        {
          value: 'Very disagreeable insight',
          id: 2,
        },
      ]}
      requestZen={action('request zen')}
      saveCurrentZen={action('save current zen')}
    />
  ));
