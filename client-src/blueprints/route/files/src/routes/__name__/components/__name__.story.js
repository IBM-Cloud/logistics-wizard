import React from 'react';
import { storiesOf, action, linkTo } from '@kadira/storybook';
import <%= pascalEntityName %> from './<%= pascalEntityName %>';

storiesOf('<%= pascalEntityName %>', module)
  .add('default state', () => (
    <<%= pascalEntityName %>
      title="Hi I am the title prop!"
      quote="Click the button to receive a quote."
      actionAndSaga={linkTo('<%= pascalEntityName %>', 'fetching quote')}
    />
  ))
  .add('fetching quote', () => (
    <<%= pascalEntityName %>
      title="You dispatched an action!"
      quote="Fetching quote..."
      actionAndSaga={linkTo('<%= pascalEntityName %>', 'quote fetched')}
    />
  ))
  .add('quote fetched', () => (
    <<%= pascalEntityName %>
      title="You dispatched an action!"
      quote="If you aren't living, then you are dying."
      actionAndSaga={linkTo('<%= pascalEntityName %>', 'additional clicks')}
    />
  ))
  .add('additional clicks', () => (
    <<%= pascalEntityName %>
      title="You already received a quote."
      quote="If you aren't living, then you are dying."
      actionAndSaga={action('No additional actions')}
    />
  ));
