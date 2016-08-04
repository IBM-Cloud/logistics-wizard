import React from 'react';
import { storiesOf, action } from '@kadira/storybook';
import Counter from './Counter';

storiesOf('Counter', module)
  .add('zero', () => (
    <Counter
      counter={0}
      doubleAsync={action('Double')}
      increment={action('Increment')}
    />
  ));
