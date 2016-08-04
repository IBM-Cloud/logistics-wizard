import React from 'react';
import { storiesOf, action } from '@kadira/storybook';
import <%= pascalEntityName %> from './<%= pascalEntityName %>';

storiesOf('<%= pascalEntityName %>', module)
  .add('zero', () => (
    <<%= pascalEntityName %>
      counter={0}
      doubleAsync={action('Double')}
      increment={action('Increment')}
    />
  ));
