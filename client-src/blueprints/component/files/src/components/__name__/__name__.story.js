import React from 'react';
import { storiesOf, action } from '@kadira/storybook';
import <%= pascalEntityName %> from './<%= pascalEntityName %>';

storiesOf('<%= pascalEntityName %>', module)
  .add('default', () => (
    <<%= pascalEntityName %>
      clicky={action('You clicked the button.')}
    />
  ))
  .add('custom prop', () => (
    <<%= pascalEntityName %>
      customProp="What a fancy example!"
      clicky={action('You clicked the button.')}
    />
  ));
